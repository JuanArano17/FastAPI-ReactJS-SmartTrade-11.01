import React from 'react';
import { Card, CardMedia, CardContent, Typography } from '@mui/material';

const SimilarProduct = ({ product }) => {
  return (
    <Card>
      <CardMedia
        component="img"
        image={product.images.length > 0 ? product.images[0].url : 'path_to_some_default_image'}
        alt={product.name}
      />
      <CardContent>
        <Typography variant="h6">{product.name}</Typography>
        <Typography variant="body2">{product.description}</Typography>
        {/* Asumiendo que la información del vendedor y el precio se encuentran en la propiedad seller_products */}
        <Typography variant="body2">{product.seller_products.length > 0 ? product.seller_products[0].seller_info : 'Seller info not available'}</Typography>
        <Typography variant="body1">Price: ${product.seller_products.length > 0 ? product.seller_products[0].price : 'Consultar'}</Typography>
      </CardContent>
    </Card>
  );
};


export default SimilarProduct;