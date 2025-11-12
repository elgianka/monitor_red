package com.agk.monitoreocom.domain.model

import kotlinx.serialization.Serializable

@Serializable
data class Estado(
    val id: Int,
    val nombre: String
)
