import React, { useEffect, useState } from 'react';
import { Card, CardMedia, CardContent, Typography, CardActions } from '@mui/material';
import FavoriteButton from '../../favorite-button/FavoriteButton';
import { getLoggedInfo } from '../../../api/services/user/profile/ProfileService';

const SummarizedProduct = ({ product }) => {
    const { idProduct, name, images, price, description, ecoPoints } = product;
    const image = images.length > 0 ? images[0] : 'default-product-image.jpg';

    const [isSeller, setIsSeller] = useState(false);

    useEffect(() => {
        const fetchUserInfo = async () => {
            const userInfo = await getLoggedInfo();
            if (userInfo.type === 'seller') {
                setIsSeller(true);
            }
        };

        fetchUserInfo();
    }, []);

    const calculateColor = (points) => {
        const red = 255 * (1 - points / 100);
        const green = 255 * (points / 100);
        const blue = 0;
        return `rgb(${Math.round(red)}, ${Math.round(green)}, ${blue})`;
    };

    const boxShadowColor = calculateColor(ecoPoints);

    return (
        <Card
            sx={{
                maxWidth: 350,
                width: '100%',
                m: 2, display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                borderRadius: '40px',
                boxShadow: '0px 4px 20px rgba(128, 128, 128, 0.4)',  
                height: '100%',
                '&:hover': {
                    boxShadow: `0px 4px 20px ${boxShadowColor}`, 
                }
            }}
        >
            <CardMedia
                component="img"
                image={image}
                alt={name}
                sx={{ height: 140, backgroundSize: 'contain' }}
            />
            <CardContent>
                {!isSeller && <FavoriteButton productId={product.id}></FavoriteButton>}
                <Typography gutterBottom variant="h6" component="div" sx={{ textAlign: 'left' }}>
                    {name}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'left' }}>
                    {description}
                </Typography>
            </CardContent>
            <CardActions sx={{ justifyContent: 'space-between', p: 2 }}>
                <Typography variant="body1" color="text.secondary" sx={{ textAlign: 'left' }}>
                    EPoints: {ecoPoints}
                </Typography>
                <Typography variant="body1" color="green" sx={{ textAlign: 'right' }}>
                    € {price.toFixed(2)}
                </Typography>
            </CardActions>
        </Card>
    );
};

export default SummarizedProduct;