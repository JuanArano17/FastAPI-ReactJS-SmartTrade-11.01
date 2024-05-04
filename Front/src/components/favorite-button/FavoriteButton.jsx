import React, { useEffect, useState } from 'react';
import { IconButton } from '@mui/material';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import StarIcon from '@mui/icons-material/Star';
import { getWishStatus, addToWishList, deleteFromWishList } from '../../api/services/products/WishListService';

const FavoriteButton = ({ productId, onToggle }) => {
    const [isFavorite, setIsFavorite] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const checkFavoriteStatus = async () => {
            setLoading(true);
            try {
                const isCurrentlyFavorite = await getWishStatus(productId);
                setIsFavorite(isCurrentlyFavorite);
            } catch (error) {
                console.error('Error al verificar el estado de favoritos', error);
            }
            setLoading(false);
        };

        checkFavoriteStatus();
    }, [productId]);

    const handleToggleFavorite = async (event) => {
        event.stopPropagation(); // Detiene la propagación del evento para que no llegue al botón padre.
        setLoading(true);
        try {
            if (!isFavorite) {
                await addToWishList(productId);
            } else {
                await deleteFromWishList(productId);
            }
            setIsFavorite(!isFavorite);
            if (onToggle) {
                onToggle();
            }
        } catch (error) {
            console.error('Error al actualizar la lista de deseos', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <IconButton 
            onClick={handleToggleFavorite}
            disabled={loading}
            sx={{ position: 'absolute', top: 8, right: 8, backgroundColor: 'background.paper', borderRadius: '50%' }}
        >
            {isFavorite ? <StarIcon sx={{ color: "#ffcc00" }} /> : <StarBorderIcon />}
        </IconButton>
    );
};
export default FavoriteButton;

