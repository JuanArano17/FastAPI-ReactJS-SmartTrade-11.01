import React, { useEffect, useState } from 'react';
import { IconButton } from '@mui/material';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import StarIcon from '@mui/icons-material/Star';
import { getFavoriteStatus, addToWishList, deleteFromWishList } from '../api/services/products/WishListService';

const FavoriteButton = ({ productId }) => {
    const [isFavorite, setIsFavorite] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const checkFavoriteStatus = async () => {
            setLoading(true);
            try {
                const status = await getFavoriteStatus(productId);
                setIsFavorite(status);
            } catch (error) {
                console.error('Error al verificar el estado de favoritos', error);
            }
            setLoading(false);
        };

        checkFavoriteStatus();
    }, [productId]);

    const handleToggleFavorite = async () => {
        setLoading(true);
        try {
            if (!isFavorite) {
                await addToWishList(productId);
            } else {
                await deleteFromWishList(productId);
            }
            setIsFavorite(!isFavorite);
        } catch (error) {
            console.error('Error al actualizar la lista de deseos', error);
        }
        setLoading(false);
    };

    return (
        <IconButton onClick={handleToggleFavorite} disabled={loading}>
            {isFavorite ? <StarIcon sx={{ color: "#ffcc00" }} /> : <StarBorderIcon />}
        </IconButton>
    );
};

export default FavoriteButton;
