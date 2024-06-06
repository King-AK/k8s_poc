package com.kingak.flinkIngestor.utils.JSON4SSerializers

import org.apache.flink.api.common.typeinfo.TypeInformation
import org.json4s.{CustomSerializer, JString}

import java.sql.Timestamp


object TimestampSerializer extends CustomSerializer[Timestamp](_ =>
      (
        { case JString(str) =>
          Timestamp.valueOf(str)
        },
        { case timestamp: Timestamp =>
          JString(timestamp.toString)
        }
      )
    )