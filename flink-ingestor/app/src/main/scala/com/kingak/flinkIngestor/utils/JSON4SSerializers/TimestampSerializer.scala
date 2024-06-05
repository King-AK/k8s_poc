package com.kingak.flinkIngestor.utils.JSON4SSerializers

import org.json4s.{CustomSerializer, JString}

import java.sql.Timestamp

object TimestampSerializer
    extends CustomSerializer[Timestamp](format =>
      (
        { case JString(str) =>
          Timestamp.valueOf(str)
        },
        { case timestamp: Timestamp =>
          JString(timestamp.toString)
        }
      )
    )
