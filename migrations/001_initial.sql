-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    category VARCHAR(100) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    attributes JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create outbox table
CREATE TABLE IF NOT EXISTS outbox (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(50) NOT NULL,
    payload JSONB NOT NULL,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE
);

-- Create trigger function and triggers (from src/triggers.sql)
CREATE OR REPLACE FUNCTION notify_product_change() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO outbox (event_type, payload) VALUES ('product.created', jsonb_build_object('product_id', NEW.id, 'data', row_to_json(NEW)));
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO outbox (event_type, payload) VALUES ('product.updated', jsonb_build_object('product_id', NEW.id, 'data', row_to_json(NEW)));
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO outbox (event_type, payload) VALUES ('product.deleted', jsonb_build_object('product_id', OLD.id));
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS product_change_trigger ON products;
CREATE TRIGGER product_change_trigger
AFTER INSERT OR UPDATE OR DELETE ON products
FOR EACH ROW EXECUTE FUNCTION notify_product_change();
