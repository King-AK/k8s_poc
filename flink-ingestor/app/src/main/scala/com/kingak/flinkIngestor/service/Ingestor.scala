package com.kingak.flinkIngestor.service

import com.kingak.flinkIngestor.schemas.StockData
import com.kingak.flinkIngestor.utils.JSON4SSerializers.TimestampSerializer
import com.typesafe.scalalogging.LazyLogging
import org.apache.flink.api.common.accumulators.IntCounter
import org.apache.flink.api.common.eventtime.WatermarkStrategy
import org.apache.flink.api.common.functions.RichMapFunction
import org.apache.flink.api.common.serialization.SimpleStringSchema
import org.apache.flink.api.common.typeinfo.TypeInformation
import org.apache.flink.connector.kafka.source.KafkaSource
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer
import org.apache.flinkx.api._
import org.apache.flinkx.api.serializers._
import org.json4s.jackson.JsonMethods._
import org.json4s.{DefaultFormats, Formats}
import scopt.{OParser, OParserBuilder}

object Ingestor extends LazyLogging {

  case class Config(
      kafkaBootstrapServers: String = "",
      topic: String = ""
  )

  val builder: OParserBuilder[Config] = OParser.builder[Config]
  val argParser: OParser[Unit, Config] = {
    import builder._
    OParser.sequence(
      programName("Ingestor"),
      head("Ingestor", "0.1"),
      opt[String]('k', "kafkaBootstrapServers")
        .action((x, c) => c.copy(kafkaBootstrapServers = x))
        .text("Kafka bootstrap servers"),
      opt[String]('t', "topic")
        .action((x, c) => c.copy(topic = x))
        .text("Kafka topic")
    )
  }

  implicit val typeInfo: Typeclass[StockData] =
    TypeInformation.of(classOf[StockData])

  val runningAvg: RichMapFunction[StockData, StockData] =
    new RichMapFunction[StockData, StockData] {
      var avg: Double = 0.0;
      val count: IntCounter = new IntCounter();
      override def map(value: StockData): StockData = {
        // update running average and count
        avg =
          (avg * count.getLocalValue + value.volume) / (count.getLocalValue + 1)
        count.add(1)
        value.copy(volume = avg)
      }
    }

  def main(args: Array[String]): Unit = {
    OParser.parse(argParser, args, Config()) match {
      case Some(config) =>
        logger.info(s"Kafka bootstrap servers: ${config.kafkaBootstrapServers}")
        logger.info(s"Kafka topic: ${config.topic}")

        val env = StreamExecutionEnvironment.getExecutionEnvironment
        val kafkaSource = KafkaSource
          .builder()
          .setBootstrapServers(config.kafkaBootstrapServers)
          .setTopics(config.topic)
          .setStartingOffsets(OffsetsInitializer.earliest())
          .setValueOnlyDeserializer(new SimpleStringSchema)
          .build()
        val data: DataStream[String] = env.fromSource(
          kafkaSource,
          WatermarkStrategy.noWatermarks[String],
          "Kafka Source"
        )
        logger.info("Data source created")
        // print running sum of volume for each symbol
        val result = data
          .map { json =>
            implicit val formats: Formats =
              DefaultFormats ++ List(TimestampSerializer)
            parse(json).extract[StockData]
          }
          .keyBy(_.symbol)
          .map(runningAvg)

        result.print()
        env.execute("Ingestor")

      case _ =>
        logger.error("Failed to parse command line arguments")
        sys.exit(1)
    }
  }
}
