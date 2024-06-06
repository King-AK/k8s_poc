package com.kingak.flinkIngestor.Basics

import com.kingak.flinkIngestor.utils.CollectSink
import org.apache.flinkx.api._
import org.apache.flinkx.api.serializers._
import org.junit.runner.RunWith
import org.scalatest.BeforeAndAfterEach
import org.scalatest.funsuite.AnyFunSuite
import org.scalatestplus.junit.JUnitRunner

@RunWith(classOf[JUnitRunner])
class TestFlinkWorks extends AnyFunSuite with BeforeAndAfterEach {

  test("Flink works") {
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    assert(env != null)
  }

  test("Flink map works") {
    val env = StreamExecutionEnvironment.getExecutionEnvironment

    // configure your test environment
    env.setParallelism(2)

    // values are collected in a static variable
    CollectSink.values.clear()

    env
      .fromElements(2)
      .map(_ + 1)
      .addSink(new CollectSink)

    // execute
    env.execute()

    // verify
    assert(CollectSink.values.get(0) == 3)
  }

}
