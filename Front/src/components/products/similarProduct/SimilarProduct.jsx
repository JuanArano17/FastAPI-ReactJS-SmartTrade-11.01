import React from 'react';
import { Card, CardContent, CardMedia, Typography, CardActions, ButtonBase } from '@mui/material';
import { useHistory } from 'react-router-dom';

const SimilarProduct = ({ product }) => {
    const history = useHistory();

    const handleProductClick = () => {
        history.push(`/catalog/product/${product.id}`);
    };

    const calculateColor = (points) => {
        const red = 255 * (1 - points / 100);
        const green = 255 * (points / 100);
        const blue = 0;
        return `rgb(${Math.round(red)}, ${Math.round(green)}, ${blue})`;
    };

    const ecoPointsColor = calculateColor(product.ecoPoints);

    return (
        <ButtonBase
            onClick={handleProductClick}
            sx={{
                width: '100%',
                textAlign: 'left',
                '&:hover .MuiCard-root': {
                    boxShadow: `0px 4px 20px ${ecoPointsColor}`, 
                    transform: 'scale(1.05)', 
                }
            }}
        >
            <Card
                className="MuiCard-root"
                sx={{
                    maxWidth: 345,
                    width: '100%',
                    minHeight: 360,
                    m: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    borderRadius: '40px',
                    boxShadow: '0px 4px 20px rgba(128, 128, 128, 0.4)',
                    transition: 'transform 0.3s, box-shadow 0.3s',
                }}
            >
                <CardMedia
                    component="img"
                    height="140"
                    image={product.images.length > 0 ? product.images[0] : 'default-product-image.jpg'}
                    alt={product.name}
                />
                <CardContent sx={{ flexGrow: 1, overflow: 'hidden' }}>
                    <Typography gutterBottom variant="h5" component="div">
                        {product.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        {product.description}
                    </Typography>
                </CardContent>
                <CardActions sx={{ justifyContent: 'space-between', p: 2 }}>
                    <Typography variant="body1" sx={{ textAlign: 'left', color: ecoPointsColor }}>
                        EcoPoints: {product.ecoPoints}
                    </Typography>
                    <Typography variant="body1" color="green" sx={{ textAlign: 'right' }}>
                        € {product.price.toFixed(2)}
                    </Typography>
                </CardActions>
            </Card>
        </ButtonBase>
    );
};

export default SimilarProduct;
