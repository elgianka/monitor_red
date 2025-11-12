package com.agk.monitoreocom.data.remote

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.json.Json

object ApiClient {

    private const val BASE_URL = "http://127.0.0.1:8000" // TODO: Cambiar por la IP de la API

    val client = HttpClient(CIO) {
        install(ContentNegotiation) {
            json(Json {
                ignoreUnknownKeys = true
                isLenient = true
                prettyPrint = true
            })
        }
    }

    fun getUrl(path: String): String {
        return BASE_URL + path
    }
}
