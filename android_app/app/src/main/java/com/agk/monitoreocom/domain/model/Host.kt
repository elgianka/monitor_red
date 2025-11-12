package com.agk.monitoreocom.domain.model

import com.agk.monitoreocom.domain.model.Estado
import com.agk.monitoreocom.domain.model.Ubicacion
import kotlinx.serialization.Serializable

@Serializable
data class Host(
    val idHost: Int,
    val nomHost: String,
    val ipHost: String,
    val macHost: String?,
    val numSerie: String?,
    val firmwareVersion: String?,
    val fechaAlta: String?,
    val anhoAlta: Int?,
    val idModelo: Int,
    val idResponsable: Int,
    val idProceso: Int,
    val idCategoria: Int,
    val estado: Estado?,
    val ubicacion: Ubicacion?,
    val limSupPing: Float?,
    val limInfPing: Float?
)
