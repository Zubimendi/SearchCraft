-- Function to insert into outbox on product change
CREATE OR REPLACE FUNCTION notify_product_change()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO outbox (event_type, payload)
        VALUES ('product.created', jsonb_build_object('product_id', NEW.id, 'data', row_to_json(NEW)));
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO outbox (event_type, payload)
        VALUES ('product.updated', jsonb_build_object('product_id', NEW.id, 'data', row_to_json(NEW)));
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO outbox (event_type, payload)
        VALUES ('product.deleted', jsonb_build_object('product_id', OLD.id));
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers on products table (assumes products table exists)
CREATE TRIGGER product_change_trigger
AFTER INSERT OR UPDATE OR DELETE ON products
FOR EACH ROW EXECUTE FUNCTION notify_product_change();
