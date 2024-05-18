import React, { useEffect, useState } from 'react';
import { Card, CardMedia, CardContent, Typography, CardActions, ButtonBase } from '@mui/material';
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

    const ecoPointsColor = calculateColor(ecoPoints);

    return (
        <ButtonBase
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
                    image={image}
                    alt={name}
                    sx={{ height: 140, backgroundSize: 'contain' }}
                />
                <CardContent sx={{ flexGrow: 1, overflow: 'hidden' }}>
                    {!isSeller && <FavoriteButton productId={product.id}></FavoriteButton>}
                    <Typography gutterBottom variant="h6" component="div" sx={{ textAlign: 'left' }}>
                        {name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'left' }}>
                        {description}
                    </Typography>
                </CardContent>
                <CardActions sx={{ justifyContent: 'space-between', p: 2 }}>
                    <Typography variant="body1" sx={{ textAlign: 'left', color: ecoPointsColor }}>
                        EcoPoints: {ecoPoints}
                    </Typography>
                    <Typography variant="body1" color="green" sx={{ textAlign: 'right' }}>
                        € {price.toFixed(2)}
                    </Typography>
                </CardActions>
            </Card>
        </ButtonBase>
    );
};

export default SummarizedProduct;
