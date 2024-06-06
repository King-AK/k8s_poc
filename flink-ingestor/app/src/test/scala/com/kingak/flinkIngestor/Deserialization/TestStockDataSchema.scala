package com.kingak.flinkIngestor.Deserialization

import com.kingak.flinkIngestor.schemas.StockData
import com.kingak.flinkIngestor.schemas.StockDataTypeInfo._
import com.kingak.flinkIngestor.utils.JSON4SSerializers.TimestampSerializer
import com.kingak.flinkIngestor.utils.StockDataSink
import org.apache.flinkx.api.StreamExecutionEnvironment
import org.apache.flinkx.api.serializers._
import org.json4s._
import org.json4s.jackson.JsonMethods._
import org.junit.runner.RunWith
import org.scalatest.BeforeAndAfterEach
import org.scalatest.funsuite.AnyFunSuite
import org.scalatestplus.junit.JUnitRunner

@RunWith(classOf[JUnitRunner])
class TestStockDataSchema extends AnyFunSuite with BeforeAndAfterEach {

  test("StockData case class can be deserialized from JSON") {
    implicit val formats: Formats = DefaultFormats ++ List(TimestampSerializer)

    val json =
      """
        |{
        |"symbol":"AAPL",
        |"datetime":"2021-01-01 00:00:00",
        |"open": "100.0",
        |"high": "110.0",
        |"low": "90.0",
        |"close": "105.0",
        |"volume": 1000
        |}""".stripMargin
    val data: StockData = parse(json).extract[StockData]
    assert(data.symbol == "AAPL")
    assert(data.datetime == java.sql.Timestamp.valueOf("2021-01-01 00:00:00"))
    assert(data.open == "100.0")
    assert(data.high == "110.0")
    assert(data.low == "90.0")
    assert(data.close == "105.0")
    assert(data.volume == 1000)
  }

  test("StockData transforms behave as expected") {
    val jsonByteSeq = Seq(
      """
        |{
        |"symbol":"AAPL",
        |"datetime":"2024-06-04 19:59:00",
        |"open": "100.0",
        |"high": "110.0",
        |"low": "90.0",
        |"close": "105.0",
        |"volume": 1000
        |}""".stripMargin
    )

    val env = StreamExecutionEnvironment.getExecutionEnvironment

    // configure your test environment
    env.setParallelism(2)

    // values are collected in a static variable
    StockDataSink.values.clear()

    val source = env.fromCollection(jsonByteSeq)
    val result = source.map { json =>
      implicit val formats: Formats =
        DefaultFormats ++ List(TimestampSerializer)
      parse(json).extract[StockData]
    }
    result.addSink(new StockDataSink)

    // execute
    env.execute()

    // verify
    assert(StockDataSink.values.get(0).symbol == "AAPL")
    assert(
      StockDataSink.values.get(0).datetime == java.sql.Timestamp.valueOf(
        "2024-06-04 19:59:00"
      )
    )

  }

}
