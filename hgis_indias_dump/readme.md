Collection of tables from HGIS de las Indias.
Includes:
    Territorios_ids: one row for each jurisdiction, province, kingdom etc. in the database "Paraguay, Provincia, RPL"
    Territorios_instancias: concrete instances of these territories, can be several per key: "Gobernacion de Paraguay", luego "Intendencia de Paraguay" etc.
    Fuentes: Lists sources used to compile HGIS de las Indias
    Territorios_fuentes_usadas: Lists sources, by type, that give information on territories. Column "foco" shows the entity is the main focus of the source (E.g. for Alcedo, that would be "America"; for Villaseñor y Sánchez "New Spain", for Azara's "description of the provinces of Paraguay and Río de la Plata" those provinces.
    Lugares_id: One row for each settlement in the database. The "Partido", "Provincia" and "Region" are only for disambiguation; of course that could actually change over time. 
    Lugares_instancias: Concrete instances of those settlements, whenever an aspect changes; e.g. pueblo de indios becomes ciudad; settlement relocated (other coordinates) after earthquake; settlement becomes parish...
    Lugares_parte_de_territorio: Tracks what provinces/bishoprics etc. a place was part of over time - should be handy for matching!
    Lugares_matches_gazetteers: Known matches between my gazetteer and WHGazetteer, Geonames, Wikidata, TGN, VIAF, and others.
    
    I will make a table that more likely matches settlements to provinces as Alcedo mentions them, for easier matching...
