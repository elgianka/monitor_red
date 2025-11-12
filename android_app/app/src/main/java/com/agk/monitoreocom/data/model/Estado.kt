package com.agk.monitoreocom.data.model

import kotlinx.serialization.Serializable

@Serializable
data class Estado(
    val ID_ESTADO: Int,
    val NOM_ESTADO: String
)
