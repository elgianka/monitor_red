package com.empresa.monitoreocom.domain.model

import kotlinx.serialization.Serializable

@Serializable
data class Estado(
    val ID_ESTADO: Int,
    val NOM_ESTADO: String
)
