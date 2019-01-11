Script de automatización de docker para decide-ganimedes para Linux:
--------------------------------------------------------------------

Introducción:
-------------

 Este script automatiza varias de las acciones más cotidianas de docker en Linux. Dichas funciones se resumen a continuación:

  - Comprobación del estado del demonio de docker (dockerd)
  - Eliminación de componentes sin uso de docker
  - Creación de usuarios de administración para web
  - Listado de imágenes, contenedores, volúmenes y redes
  - Compilado, encendido y apagado con docker-compose


¿Cómo utilizar?:
----------------

 Simplemente bastará con dar permisos de ejecución al script. Bastará con ejecutar el siguiente comando:

      chmod 777 dockerManager.sh

 Por último, ejecutamos el script de la siguiente forma:

      ./dockerManager.sh


Interfaz de usuario:
--------------------

 El script controla el estado en el que se encuentra el demonio de docker. Dependiendo del estado en el que se encuentre permitirá unas acciones u otras.

 +----------------------------------------------------------------------+     +----------------------------------------------------------------------+
 |              Panel de Administración - Decide-Ganimedes              |     |              Panel de Administración - Decide-Ganimedes              |
 +----------------------------------------------------------------------+     +----------------------------------------------------------------------+
 | 1) Activar demonio de docker                                         |     | 1) Activar demonio de docker                                         |   
 |                                                                      |     |                                                                      |
 | Estado del demonio de docker: INACTIVO                               |     | Si la activación del demonio de docker ha fallado puede ser debido a |
 |                                                                      |     | que el servicio se ha activado y apagado demasiadas veces de forma   |
 | 0)  Salir                                                            |     | muy rápida. Espere 1 minuto para volver a intentarlo.                |
 |                                                                      |     |                                                                      |
 +----------------------------------------------------------------------+     | Estado del demonio de docker: FALLIDO                                |
 									      |                                                                      |							
 									      | 0)  Salir                                                            |
 									      |                                                                      | 
									      +----------------------------------------------------------------------+
+----------------------------------------------------------------------+
|              Panel de Administración - Decide-Ganimedes              |
+----------------------------------------------------------------------+
| 1) Listar imágenes, contenedores, volúmenes y redes                  |
| 2) Eliminar componentes de docker sin uso                            |
|                                                                      |
| 3) Encender contenedores con docker-compose                          |
| 4) Compilar contenedores con docker-compose                          |
| 5) Apagar contenedores con docker-compose                            |
| 6) Eliminar contenedores con docker-compose                          |
| 7) Visualizar logs con docker-compose                                |
|                                                                      |
| 8) Crear un usuario de administración para web                       |
|                                                                      |
| 9) Desactivar demonio de docker                                      |
|                                                                      |
| Estado del demonio de docker: ACTIVO                                 |
|                                                                      |
| 0)  Salir                                                            |
|                                                                      |
+----------------------------------------------------------------------+

 

Acciones que permite el script:
-------------------------------

A continuación se detallan cada una de las acciones con el demonio de Docker ACTIVO:

 1) Listar imágenes, contenedores, volúmenes y redes: muestra información de las imágenes, contenedores, volúmenes y redes desplegadas en el sistema.
 2) Eliminar componentes de docker: despliega un menú que permite escoger qué elementos sin uso podemos eliminar.
 3) Encender contenedores con docker-compose: su propio nombre lo explica.
 4) Compilar contenedores con docker-compose: su propio nombre lo explica. 
 5) Apagar contenedores con docker-compose: su propio nombre lo explica.
 6) Eliminar contenedores con docker-compose: su propio nombre lo explica.
 7) Visualizar logs con docker-compose: su propio nombre lo indica. Permite elegir que se muestren los logs en vivo.
 8) Crear un usuario de administración para web: permite crear un usuario de administración en la web de docker basada en Django.
 9) Desactivar demonio de Docker: su propio nombre lo explica. 

A continuación se detallan cada una de las acciones con el demonio de Docker INACTIVO:

 1) Activar demonio de Docker: su propio nombre lo explica.

A continuación se detallan cada una de las acciones con el demonio de Docker FALLIDO:

 1) Activar demonio de Docker: su propio nombre lo explica. Incluye una nota explicando el motivo por el que ha podido fallar basándome en mi experiencia.

