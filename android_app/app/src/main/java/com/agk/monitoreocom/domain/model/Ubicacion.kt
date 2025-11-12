package com.agk.monitoreocom.domain.model

import kotlinx.serialization.Serializable

@Serializable
data class Ubicacion(
    val id: Int,
    val nombre: String
)
