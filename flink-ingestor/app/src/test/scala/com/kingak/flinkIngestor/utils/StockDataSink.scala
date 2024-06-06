package com.kingak.flinkIngestor.utils

import com.kingak.flinkIngestor.schemas.StockData
import org.apache.flink.streaming.api.functions.sink.SinkFunction

import java.util
import java.util.Collections

// create a testing sink for StockData
class StockDataSink extends SinkFunction[StockData] {

  override def invoke(value: StockData, context: SinkFunction.Context): Unit = {
    StockDataSink.values.add(value)
  }
}

object StockDataSink {
  // must be static
  val values: util.List[StockData] =
    Collections.synchronizedList(new util.ArrayList[StockData]())
}
