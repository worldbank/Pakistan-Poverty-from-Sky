# Extract OSM Roads to BISP Households

buffer_size_osm_m <- c(100, 200, 1000, 2000, 5000, 10000)

# Load Data --------------------------------------------------------------------
#### Roads
osm_roads_sdf <- readRDS(file.path(project_file_path, "Data", "OSM", "FinalData - Cleaned", "gis_osm_roads_free_1.Rds"))

#### OSM Coordinates
opm_coords <- readRDS(SURVEY_COORDS_PATH)

coordinates(opm_coords) <- ~longitude+latitude
crs(opm_coords) <- CRS("+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0")

# Reproject Data ---------------------------------------------------------------
osm_roads_sdf <- spTransform(osm_roads_sdf, CRS(PAK_UTM_PROJ))
opm_coords    <- spTransform(opm_coords, CRS(PAK_UTM_PROJ))

## To sf
osm_roads_sf        <- osm_roads_sdf      %>% st_as_sf()
# opm_coords_buff100m <- opm_coords_buff100m %>% st_as_sf()
# opm_coords_buff200m <- opm_coords_buff200m %>% st_as_sf()
# opm_coords_buff1km  <- opm_coords_buff1km %>% st_as_sf()
# opm_coords_buff2km  <- opm_coords_buff2km %>% st_as_sf()
# opm_coords_buff5km  <- opm_coords_buff5km %>% st_as_sf()

# Length of Roads of Different Types -------------------------------------------
extract_road_length <- function(road_type, osm_roads_sf, buffer_sf){
  
  print(paste(road_type," =============="))
  
  ## Subset roads to road type and cut up so only in buffered portions
  # TODO: distance faster than intersection?
  buffer_sf_agg <- buffer_sf %>% st_union()
  osm_roads_sf_typei <- osm_roads_sf[osm_roads_sf$fclass %in% road_type,]
  osm_roads_sf_typei_subset <- st_intersection_chunks(osm_roads_sf_typei, buffer_sf_agg, 2000)
  
  ## Loop through buffers and extract road length
  road_length <- lapply(1:nrow(buffer_sf), function(i){
    print(paste0(i, " - Extracting Length: ", road_type))
    
    intersects_tf <- st_intersects(opm_coords_buff[i,], osm_roads_sf_typei_subset, sparse = F) %>% as.vector()
    road_in_buffer <- st_intersection(osm_roads_sf_typei_subset[intersects_tf,], opm_coords_buff[1,])
    
    if(nrow(road_in_buffer) > 0){
      out <- road_in_buffer %>% st_length() %>% sum() %>% as.numeric()
    } else{
      out <- 0
    }
    
    return(out)
  }) %>% unlist()
  
  ## Cleanup output
  buffer_sf[[road_type]] <- road_length
  out_df <- buffer_sf[,c("uid", road_type)]
  out_df$geometry <- NULL
  
  return(out_df)
}

# Implement and Export ---------------------------------------------------------
for(buffer_size_m_i in buffer_size_osm_m){
  print(paste(buffer_size_m_i, "---------------------------------------------"))
  
  opm_coords_buff  <- gBuffer(opm_coords, width = buffer_size_m_i, byid = T) %>% st_as_sf()
  
  rd_length_m_df <- lapply(unique(osm_roads_sf$fclass),
                             extract_road_length,
                             osm_roads_sf,
                             opm_coords_buff) %>%
    reduce(merge, by = "uid") %>%
    dplyr::rename_at(vars(-uid), ~ paste0("osm_length_", ., "_",buffer_size_m_i,"m_buff"))
  
  saveRDS(rd_length_m_df, file.path(project_file_path, "Data", SURVEY_NAME, "FinalData", "Individual Datasets", paste0("osm_road_length_",buffer_size_m_i,"m_buff.Rds")))
  write.csv(rd_length_m_df, file.path(project_file_path, "Data", SURVEY_NAME, "FinalData", "Individual Datasets", paste0("osm_road_length_",buffer_size_m_i,"m_buff.csv")),
            row.names = F)
  
}

