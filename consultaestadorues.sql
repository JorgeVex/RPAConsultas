-- -- phpMyAdmin SQL Dump
-- -- version 5.2.1
-- -- https://www.phpmyadmin.net/
-- --
-- -- Servidor: 127.0.0.1
-- -- Tiempo de generación: 24-01-2024 a las 20:15:52
-- -- Versión del servidor: 10.4.32-MariaDB
-- -- Versión de PHP: 8.2.12

-- SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
-- START TRANSACTION;
-- SET time_zone = "+00:00";


-- /*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
-- /*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
-- /*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
-- /*!40101 SET NAMES utf8mb4 */;

-- --
-- -- Base de datos: `consultaestadorues`
-- --

-- -- --------------------------------------------------------

-- --
-- -- Estructura de tabla para la tabla `consultarr`
-- --

-- CREATE TABLE `consultarr` (
--   `idconsultarr` int(11) NOT NULL,
--   `Proveedor` varchar(45) DEFAULT NULL,
--   `FechaConsultaRUT` datetime DEFAULT NULL,
--   `ProveedorId` varchar(45) DEFAULT NULL,
--   `ProveedorDv` varchar(45) DEFAULT NULL
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- -- --------------------------------------------------------

-- --
-- -- Estructura de tabla para la tabla `proveedorrues`
-- --

-- CREATE TABLE `proveedorrues` (
--   `ProvNit` int(11) NOT NULL,
--   `ProvNombre` varchar(45) NOT NULL,
--   `FechaRegistro` datetime NOT NULL,
--   `FechaUltimaActualizacion` datetime NOT NULL,
--   `Estado` varchar(40) NOT NULL,
--   `CamaraComercio` varchar(45) NOT NULL,
--   `Matricula` int(45) NOT NULL,
--   `OrganizacionJuridica` varchar(45) NOT NULL,
--   `Categoria` varchar(255) DEFAULT NULL,
--   `ActividadesEconomicas` varchar(255) NOT NULL
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- -- --------------------------------------------------------

-- --
-- -- Estructura de tabla para la tabla `proveedorrut`
-- --

-- CREATE TABLE `proveedorrut` (
--   `idProveedorRUT` int(11) NOT NULL,
--   `NombreRUT` varchar(45) DEFAULT NULL,
--   `DvRUT` varchar(45) DEFAULT NULL,
--   `EstadoRUT` varchar(45) DEFAULT NULL
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --
-- -- Índices para tablas volcadas
-- --

-- --
-- -- Indices de la tabla `consultarr`
-- --
-- ALTER TABLE `consultarr`
--   ADD PRIMARY KEY (`idconsultarr`);

-- --
-- -- Indices de la tabla `proveedorrues`
-- --
-- ALTER TABLE `proveedorrues`
--   ADD PRIMARY KEY (`ProvNit`);

-- --
-- -- Indices de la tabla `proveedorrut`
-- --
-- ALTER TABLE `proveedorrut`
--   ADD PRIMARY KEY (`idProveedorRUT`);

-- --
-- -- AUTO_INCREMENT de las tablas volcadas
-- --

-- --
-- -- AUTO_INCREMENT de la tabla `consultarr`
-- --
-- ALTER TABLE `consultarr`
--   MODIFY `idconsultarr` int(11) NOT NULL AUTO_INCREMENT;

-- --
-- -- AUTO_INCREMENT de la tabla `proveedorrut`
-- --
-- ALTER TABLE `proveedorrut`
--   MODIFY `idProveedorRUT` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1001298960;
-- COMMIT;

-- /*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
-- /*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
-- /*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
