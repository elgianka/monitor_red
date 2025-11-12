package com.agk.monitoreocom.domain.repository

import com.agk.monitoreocom.domain.model.Host

/**
 * Esta es la interfaz del Repositorio.
 * Define un "contrato" de lo que la capa de datos DEBE ser capaz de hacer.
 * La capa de dominio no sabe (ni le importa) si los datos vienen de una API,
 * una base de datos local o un archivo de texto.
 */
interface HostRepository {

    /**
     * Obtiene una lista de todos los hosts desde la fuente de datos.
     */
    suspend fun getHosts(): List<Host>

}
