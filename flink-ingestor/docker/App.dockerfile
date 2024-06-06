FROM gradle:8.7.0-jdk8-focal AS gradleBuild
COPY --chown=gradle:gradle . /home/gradle/src
WORKDIR /home/gradle/src
RUN gradle clean build --no-daemon

FROM flink:1.19.0-java11
# Clean out /opt/flink/lib/flink-scala_2.12-1.19.0.jar to avoid conflicts with the Scala 2.13 version
# Deprecated my ass
RUN rm /opt/flink/lib/flink-scala*.jar
COPY --from=gradleBuild /home/gradle/src/app/build/libs/* /opt/flink/usrlib/artifacts/