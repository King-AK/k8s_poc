package Utils

import org.apache.flink.streaming.api.functions.sink.SinkFunction

import java.util
import java.util.Collections

// create a testing sink
class CollectSink extends SinkFunction[Int] {

  override def invoke(value: Int, context: SinkFunction.Context): Unit = {
    CollectSink.values.add(value)
  }
}

object CollectSink {
  // must be static
  val values: util.List[Int] =
    Collections.synchronizedList(new util.ArrayList[Int]())
}
