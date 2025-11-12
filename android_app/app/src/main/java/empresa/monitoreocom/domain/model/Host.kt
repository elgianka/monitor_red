package com.agk.monitoreo.com.domain.model

import kotlinx.serialization.Serializable

@Serializable
data class Host(
    val id: Int,
    val nombre: String,
    val ip: String,
    val estado_id: Int? = null,
    val categoria_id: Int? = null,
    val ubicacion_id: Int? = null,
    val marca_id: Int? = null,
    val modelo_id: Int? = null,
    val responsable_id: Int? = null,
    val proceso_id: Int? = null,
    val area_id: Int? = null,
    val gerencia_id: Int? = null,
    val sede_id: Int? = null,
    val numero_serie: String? = null,
    val codigo_inventario: String? = null,
    val observaciones: String? = null,
    val fecha_adquisicion: String? = null,
    val fecha_instalacion: String? = null,
    val fecha_ultimo_mantenimiento: String? = null,
    val fecha_proximo_mantenimiento: String? = null
)
