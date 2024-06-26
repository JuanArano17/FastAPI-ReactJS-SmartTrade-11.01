import React, { useState, useEffect } from 'react';
import { Box, Container, Grid, Paper, Typography, Button, Pagination } from '@mui/material';
import { useHistory, useParams } from 'react-router-dom';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import SummarizedProduct from '../components/products/summarizedProduct/SummarizedProduct';
import FilterProducts from '../components/products/filterProducts/FilterProducts';
import styles from '../styles/styles';
import { getAllProductsSeller } from '../api/services/products/ProductsService';

const CatalogPage = () => {
    const { search } = useParams();
    const [searchTerm, setSearchTerm] = useState(search || "");
    const [products, setProducts] = useState([]);
    const [searchFilteredProducts, setSearchFilteredProducts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const productsPerPage = 12;
    const history = useHistory();

    useEffect(() => {
        setSearchTerm(search || "");
    }, [search]);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                setLoading(true);
                const productsWithSellers = await getAllProductsSeller();
                setProducts(productsWithSellers);
                setLoading(false);
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };

        fetchProducts();
    }, [searchTerm]);

    const totalPages = Math.ceil(searchFilteredProducts.length / productsPerPage);
    const indexOfLastProduct = currentPage * productsPerPage;
    const indexOfFirstProduct = indexOfLastProduct - productsPerPage;
    const currentProducts = searchFilteredProducts.slice(indexOfFirstProduct, indexOfLastProduct);

    const handleChangePage = (event, value) => {
        setCurrentPage(value);
    };

    const handleProductClick = (productId) => {
        history.push(`/catalog/product/${productId}`);
    };

    if (loading) return <Typography>Cargando...</Typography>;
    if (error) return <Typography>Error: {error}</Typography>;

    return (
        <Box sx={styles.mainBox}>
            <TopBar showSearchBar={true} showLogoutButton={true} />
            <Container sx={styles.mainContainer}>
                <Paper elevation={3} sx={styles.paperContainer}>
                    <FilterProducts products={products} setSearchFilteredProducts={setSearchFilteredProducts} searchTerm={searchTerm} />
                    <Grid container spacing={3} mt={2}>
                        {currentProducts && currentProducts.map((product) => (
                            <Grid sx={{ marginBottom: '40px' }} item xs={12} sm={4} md={4} lg={4} key={`${product.id}`}>
                                <Button
                                    onClick={() => handleProductClick(product.id)}
                                    sx={{
                                        width: '100%',
                                        height: '100%',
                                        padding: 0,
                                        '&:hover': {
                                            backgroundColor: 'transparent',
                                            boxShadow: 'none'
                                        }
                                    }}>
                                    <SummarizedProduct product={product} />
                                </Button>
                            </Grid>
                        ))}
                    </Grid>
                    <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
                        <Pagination count={totalPages} page={currentPage} onChange={handleChangePage} />
                    </Box>
                </Paper>
            </Container>
            <Footer />
        </Box>
    );
};

export default CatalogPage;
