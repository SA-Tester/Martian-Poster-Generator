-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: MarsImagery
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `image_descriptions`
--

DROP TABLE IF EXISTS `image_descriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image_descriptions` (
  `name` varchar(25) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `source` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image_descriptions`
--

LOCK TABLES `image_descriptions` WRITE;
/*!40000 ALTER TABLE `image_descriptions` DISABLE KEYS */;
INSERT INTO `image_descriptions` VALUES ('CHEMCAM','Stands for Chemistry and camera complex. CHEMCAM is present in Mars Curiosity rover to analyze chemical composition of rocks and soil. It has four components as telescope, remote micro-imager, laser and spectrometer. Telescope focus laser and the camera while micro-imager captures detailed images illuminated by the laser. The laser vaporizes rock surfaces creating a plasma of their component gases. Finally, spectrometer divide the plasma light into wavelengths for chemical analysis.','https://mars.nasa.gov/msl/spacecraft/instruments/chemcam/'),('CURIOSITY','Curiosity was designed to explore the Gale Crater and had a size of Car. The rover landed on Mars on 6 August 2012 and is operational until today (October 2022). The mission had 8 main objectives as follows: Identifying the nature of Organic carbon compounds, investigate for chemical constituents for life, identify effects of biological processes, observe mineralogical composition of Mars, interpret rock formations, assess Martian atmosphere, determine current water and Carbon dioxide cycle, and analyze radiation spectrum. Curiosity is occupied with FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI and NAVCAM cameras.','https://en.wikipedia.org/wiki/Curiosity_(rover)'),('HAZ','HAZ cameras (Hazard Avoidance Camera) are used in NASA?s Spirit, Opportunity, Curiosity and even Perseverance Rovers. Hazard Avoidance Cameras are usually return black and white image in 1024 X 1024-pixel resolution. Having a wide field of view, approximately 120 degrees both horizontally and vertically, these cameras are being used to navigate through terrains safely. Being fixed position cameras, they are able to produce 3D maps of the surroundings helping rovers to stay away from hazards. HAZ cameras and NAVCAMs are considered engineering cameras because they aren?t used by any scientific experiments assigned to the rover. Usually two HAZCAMs are place in the front and rear of a rover.','https://en.wikipedia.org/wiki/Hazcam'),('MAHLI','Stands for Mars Hand Lens Imager. This camera unit is expected to provide microscopic images of minerals, textures, rock structures and soil that are smaller than the diameter of a human hair. This also has a camera quality of a typical digital camera and shoots images in the resolution 1600X1200 pixels. MAHLI has 8GB flash storage and a SDRAM pf 128MB. This is the first ever camera unit to send scientists on Earth thumbnails so that they can choose best images. MAHLI can shoot 720p HD Video.','https://mars.nasa.gov/msl/spacecraft/instruments/mahli/'),('MARDI','MARDI stands for Mars Descent Imager. This camera?s main job was to take photographs during the spacecraft descent through the Martian atmosphere. MARDI was allocated 8GB flash memory storage which allowed to stored 400 raw frames. Having HD video capability of 4 color frames per second which is closer to 1600X1200 pixels per frame, the deployment of the unit intended to know the location of loose debris, boulders, cliffs and other features of the Martian terrain.','https://mars.nasa.gov/msl/spacecraft/instruments/mardi/'),('MAST','Stands to Mast Camera. Available in Curiosity rover to take panoramic colored photographs of surface, atmospheric features and terrain ahead of the rover. These have quality of a typical consumer camera but can take images in the resolution 1600 X 1200 pixels. MAST cameras do have a memory of 8 GB allowing several hours of HD video and raw frames to be stored. These are also capable of providing HD videos which capture 10 frames per second.','https://mars.nasa.gov/msl/spacecraft/instruments/mastcam/'),('MINITES','Miniature Thermal Emission Spectrometer (Mini-TES) or MINITES is a camera unit which was found on Spirit and Opportunity rovers. This unit was established to determine the mineralogy of rocks and soils from a distance by identifying their patterns and thermal radiation. MINI-TES unit was established inside of the rover body and weighed around 2.4 kg. Requiring 5.6W operating power this unit sized 23.5 X 16.3 X 15.5 cm.','https://mars.nasa.gov/mer/mission/instruments/mini-tes/'),('NAVCAM','NAVCAM stands for Navigational Camera. Used for navigation purposes without causing any disturbance to scientific instruments. These types of cameras take wide angle photographs which helps to decide the next move of the rover or to track objects. Curiosity rover has two pairs of navigation cameras having a 45-degree angle of view which supports ground navigation. NAVCAMs use visible light and stereoscopic 3D imagery.','https://en.wikipedia.org/wiki/Navcam'),('OPPORTUNITY','Also known as the MER-B (Mars Exploration Rover - B) or MER-1, and nicknamed Oppy, Opportunity rover spend 14 years and 136 earth days on Mars from 2004 to mid-2018. Opportunity is the twin rover of Spirit but had an extended lifetime than Spirit because Opportunity maintained its power and key systems through continual recharging of its batteries using solar power, and hibernating during events such as dust storms. The mission intended to search and characterize rocks and regolith on finding clues for past water activity, determine the distribution and composition of Martian rocks and minerals, identify geological processes and search for iron containing minerals. Due to the planetary 2018 dust storm on Mars, Opportunity ceased communications on June 10 and entered hibernation on June 12, 2018.','https://en.wikipedia.org/wiki/Opportunity_(rover)'),('PANCAM','PANCAM stands for Panoramic Camera. Mars exploration rovers Spirit and Opportunity has 2 electronics stereo cameras and one being PANCAM. Two PANCAMs are placed beside two NAVCAMS on the MER camera bar assemble. These cameras have a filter wheel that enables them to view different wavelengths of light. PANCAMs can gain an angular resolution of 300 microradians according to JPL Uncompressed stereoscopic taken by panoramas may exceed 10 GB. Spirit rover managed to take the highest resolution image taken on another planet around 2004.','https://en.wikipedia.org/wiki/Pancam'),('SPIRIT','Also known as MER-A (Mars Exploration Rover - A) or MER-2, Spirit operated on mars 6 years and 77 days from earth time, from 2004 to 2010. This landed on Gusev crater on 4th January 2004 and operated successfully until 22nd March 2010 performing stationary science as it was stuck on sand on 1st May 2009. Spirit occupied five cameras FHAZ, RHAZ, NAVCAM, PANCAM and MINITES. During its 6-year lifetime on Mars Spirit discovered the basalt on plains of Gusev, Plains and Columbian Hills. Spirit pointed its cameras towards the sky and observed a transit of the Sun by Mars\' moon Deimos (see Transit of Deimos from Mars). It also took the first photo of Earth from the surface of another planet in early March 2004.','https://en.wikipedia.org/wiki/Spirit_(rover)');
/*!40000 ALTER TABLE `image_descriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image_info`
--

DROP TABLE IF EXISTS `image_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image_info` (
  `image_id` int NOT NULL,
  `sol` int DEFAULT NULL,
  `camera` varchar(10) DEFAULT NULL,
  `path` varchar(400) DEFAULT NULL,
  `earth_date` date DEFAULT NULL,
  `rover_name` varchar(30) DEFAULT NULL,
  `rover_landing_date` date DEFAULT NULL,
  `rover_launch_date` date DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`image_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image_info`
--

LOCK TABLES `image_info` WRITE;
/*!40000 ALTER TABLE `image_info` DISABLE KEYS */;
INSERT INTO `image_info` VALUES (191613,2119,'PANCAM','processed-images/originals/camera/PANCAM - 3.png','2010-01-10','Opportunity','2004-01-25','2003-07-07','complete'),(346359,808,'PANCAM','processed-images/originals/camera/PANCAM - 1.png','2006-04-13','Spirit','2004-01-04','2003-06-10','complete'),(346360,808,'PANCAM','processed-images/originals/camera/PANCAM - 2.png','2006-04-13','Spirit','2004-01-04','2003-06-10','complete'),(362667,518,'PANCAM','processed-images/originals/rover/OPPORTUNITY - 1.png','2005-06-19','Spirit','2004-01-04','2003-06-10','complete'),(362668,518,'PANCAM','processed-images/originals/rover/OPPORTUNITY - 2.png','2005-06-19','Spirit','2004-01-04','2003-06-10','complete'),(362669,518,'PANCAM','processed-images/originals/rover/OPPORTUNITY - 3.png','2005-06-19','Spirit','2004-01-04','2003-06-10','complete');
/*!40000 ALTER TABLE `image_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `search_image`
--

DROP TABLE IF EXISTS `search_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `search_image` (
  `search_text` varchar(100) DEFAULT NULL,
  `image1` int DEFAULT NULL,
  `image2` int DEFAULT NULL,
  `image3` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search_image`
--

LOCK TABLES `search_image` WRITE;
/*!40000 ALTER TABLE `search_image` DISABLE KEYS */;
INSERT INTO `search_image` VALUES ('OPPORTUNITY',362667,362668,362669),('PANCAM',346359,346360,191613);
/*!40000 ALTER TABLE `search_image` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-02 22:46:58
