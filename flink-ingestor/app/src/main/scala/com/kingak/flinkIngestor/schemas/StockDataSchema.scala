package com.kingak.flinkIngestor.schemas

import com.kingak.flinkIngestor.utils.JSON4SSerializers.TimestampSerializer
import org.apache.flink.api.common.serialization.DeserializationSchema
import org.apache.flink.api.common.typeinfo.TypeInformation
import org.apache.flink.api.java.typeutils.TypeExtractor
import org.json4s._
import org.json4s.jackson.JsonMethods._

//import org.json4s.native.JsonMethods._

case class StockData(
                      symbol: String,
                      datetime: java.sql.Timestamp,
                      open: Double,
                      high: Double,
                      low: Double,
                      close: Double,
                      volume: Double
                    )

class StockDataSchema extends DeserializationSchema[StockData] {

  implicit val formats: Formats = DefaultFormats ++ List(TimestampSerializer)

  override def deserialize(message: Array[Byte]): StockData = {
    val jsonRecord = new String(message, "UTF-8")
    parse(jsonRecord).extract[StockData]
  }

  override def isEndOfStream(nextElement: StockData): Boolean = false

  override def getProducedType: TypeInformation[StockData] =
    TypeExtractor.getForClass(classOf[StockData])
}
