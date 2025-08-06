FROM openjdk:17
COPY ./target/D387_sample_code-0.0.2-SNAPSHOT.jar app.jar
COPY ./target/translation_en_US.properties /
COPY ./target/translation_fr_FR.properties /
EXPOSE 8080:8080
ENTRYPOINT ["java", "-jar", "app.jar"]
