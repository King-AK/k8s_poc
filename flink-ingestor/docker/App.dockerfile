FROM gradle:8.7.0-jdk8-focal AS gradleBuild
COPY --chown=gradle:gradle . /home/gradle/src
WORKDIR /home/gradle/src
RUN gradle clean build --no-daemon

FROM flink:1.19.0-scala_2.12-java8
COPY --from=gradleBuild /home/gradle/src/app/build/libs/* /opt/flink/usrlib/artifacts/