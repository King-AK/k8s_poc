package com.kingak.flinkIngestor.schemas

import org.apache.flink.api.common.typeinfo.TypeInformation
import org.apache.flinkx.api.serializers._

import java.sql.Timestamp

case class StockData(
    symbol: String,
    datetime: java.sql.Timestamp,
    open: String,
    high: String,
    low: String,
    close: String,
    volume: Double
)

object StockDataTypeInfo {
  implicit val timestampTypeInfo: TypeInformation[Timestamp] =
    TypeInformation.of(classOf[Timestamp])
  implicit val stockDataTypeInfo: TypeInformation[StockData] =
    deriveTypeInformation[StockData]
}

//class StockDataSchema extends DeserializationSchema[StockData] {
//
//  implicit val formats: Formats = DefaultFormats // ++ List(TimestampSerializer)
//StockData
//  override def deserialize(message: Array[Byte]): StockData = {
//    val jsonRecord = new String(message, "UTF-8")
//    parse(jsonRecord).extract[StockData]
//  }
//
//  override def isEndOfStream(nextElement: StockData): Boolean = false
//
//  override def getProducedType: TypeInformation[StockData] =
//    TypeExtractor.getForClass(classOf[StockData])
//}
