-- corrections table
CREATE TABLE corrections (
    id BIGSERIAL PRIMARY KEY,
    image_id TEXT NOT NULL,
    user_id TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT now(),
    original_inference JSONB NOT NULL,
    correction JSONB NOT NULL,
    status TEXT NOT NULL DEFAULT 'raw',
    validation_info JSONB,
    dataset_shard TEXT,
    processing_notes TEXT
);

-- curated dataset entries after validation
CREATE TABLE curated_examples (
    id BIGSERIAL PRIMARY KEY,
    image_id TEXT NOT NULL,
    svg TEXT,
    raster_path TEXT,
    coco_annotation JSONB,
    netlist_json JSONB,
    created_from_correction_id BIGINT REFERENCES corrections(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);