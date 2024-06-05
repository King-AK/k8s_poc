package com.kingak.flinkIngestor.Deserialization

import com.kingak.flinkIngestor.schemas.StockData
import com.kingak.flinkIngestor.utils.JSON4SSerializers.TimestampSerializer
import org.junit.runner.RunWith
import org.scalatest.BeforeAndAfterEach
import org.scalatest.funsuite.AnyFunSuite
import org.scalatestplus.junit.JUnitRunner
import org.json4s._
import org.json4s.jackson.JsonMethods._

@RunWith(classOf[JUnitRunner])
class TestStockDataSchema extends AnyFunSuite with BeforeAndAfterEach {

  implicit val formats: Formats = DefaultFormats ++ List(TimestampSerializer)

  test("StockData case class can be deserialized from JSON") {
    val json =
      """
        |{
        |"symbol":"AAPL",
        |"datetime":"2021-01-01 00:00:00",
        |"open": 100.0,
        |"high": 110.0,
        |"low": 90.0,
        |"close": 105.0,
        |"volume": 1000
        |}""".stripMargin
    val data: StockData = parse(json).extract[StockData]
    assert(data.symbol == "AAPL")
    assert(data.datetime == java.sql.Timestamp.valueOf("2021-01-01 00:00:00"))
    assert(data.open == 100.0)
    assert(data.high == 110.0)
    assert(data.low == 90.0)
    assert(data.close == 105.0)
    assert(data.volume == 1000)
  }

}
