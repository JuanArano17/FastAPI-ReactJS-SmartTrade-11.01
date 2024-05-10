import React, { useState, useEffect } from 'react';
import { Box, Container, Typography, Grid, Paper, Divider, CircularProgress, Rating, ButtonBase, Button, TextField, Dialog, DialogTitle, DialogContent, DialogActions, FormControlLabel, Switch } from '@mui/material';
import styles from '../styles/styles';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import { useParams } from 'react-router-dom';
import { getProductSellerById } from '../api/services/products/ProductsService';
import { evaluateSellerProductById } from '../api/services/products/AdminService';
import { useHistory } from 'react-router-dom';

const ValidateProductPage = () => {
    const { id } = useParams();
    const [productData, setProductData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [imageIndex, setImageIndex] = useState(0);
    const [ecoPoints, setEcoPoints] = useState('');
    const [openApprovalDialog, setOpenApprovalDialog] = useState(false);
    const [openRejectionDialog, setOpenRejectionDialog] = useState(false);
    const [ageRestriction, setAgeRestriction] = useState(false);
    const [justification, setJustification] = useState('');
    const history = useHistory();

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                setLoading(true);
                console.log("id:", id)
                const response = await getProductSellerById(id);
                if (response) {
                    setProductData(response);
                    setLoading(false);
                    setError(null);
                }
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };
        fetchProducts();
    }, [id]);
    const handleImageChange = (newIndex) => {
        setImageIndex(newIndex);
    };
    const handleOpenApprovalDialog = () => {
        setOpenApprovalDialog(true);
    };

    const handleCloseApprovalDialog = () => {
        setOpenApprovalDialog(false);
    };

    const handleOpenRejectionDialog = () => {
        setOpenRejectionDialog(true);
    };

    const handleCloseRejectionDialog = () => {
        setOpenRejectionDialog(false);
    };
    const handleApprove = async () => {
        try {
            const approvedProduct = {
                id: productData.id,
                state: "Approved",
                age_restricted: ageRestriction,
                eco_points: ecoPoints
            }
            const response = await evaluateSellerProductById(approvedProduct);
            console.log('Product validated successfully:', response);
            history.push('/admin');
        } catch (error) {
            console.error('Error validating:', error);
        }
        handleCloseApprovalDialog();
    };
    const handleReject = async () => {
        try {
            const rejectedProduct = {
                id: productData.id,
                state: "Rejected",
                justification: justification
            }
            const response = await evaluateSellerProductById(rejectedProduct);
            console.log('Product rejected successfully:', response);
            history.push('/admin');
        } catch (error) {
            console.error('Error rejecting product', error);
        }
        handleCloseRejectionDialog();
    };
    const renderAdditionalAttributes = (productData) => {
        const commonAttributes = ['name', 'description', 'id_product', 'id_seller', 'eco_points', 'spec_sheet', 'stock', 'id', 'images', 'seller_products', 'age_restricted', 'size'];
        return Object.keys(productData)
            .filter(key => !commonAttributes.includes(key))
            .map(key => (
                <Paper key={key} elevation={1} sx={{ margin: '10px 0', padding: '10px' }}>
                    <Typography variant="body2" color="text.secondary" component="span">
                        {`${key.charAt(0).toUpperCase() + key.slice(1)}: `}
                    </Typography>
                    <Typography variant="body2" component="span" sx={{ fontWeight: 'bold' }}>
                        {productData[key]}
                    </Typography>
                </Paper>
            ));
    };
    if (loading) {
        return <CircularProgress />;
    }
    if (error) {
        return <Typography color="error">{error}</Typography>;
    }
    return (
        <Box sx={styles.mainBox}>
            <TopBar showSearchBar={true} showLogoutButton={true} />
            <Container sx={styles.mainContainer}>
                {productData && (
                    <Paper elevation={3} sx={{ ...styles.paperContainer, position: 'relative' }}>
                        <Grid container spacing={2}>
                            <Grid item xs={12} md={5} sx={{ display: 'flex', justifyContent: 'center' }}>
                                <Box sx={{ width: '100%', height: 300, display: 'flex', justifyContent: 'center', alignItems: 'center', overflow: 'hidden' }}>
                                    <ButtonBase onClick={() => handleImageChange((imageIndex + 1) % productData.images.length)} disabled={productData.images.length <= 1}>
                                        <img
                                            src={productData.images[imageIndex]}
                                            alt={`Image ${imageIndex + 1} of ${productData.name}`}
                                            style={{ maxWidth: '100%', maxHeight: '100%', width: 'auto', height: 'auto' }}
                                        />
                                    </ButtonBase>
                                </Box>
                            </Grid>
                            <Grid item xs={12} md={7}>
                                <Typography variant="h6" color="text.secondary">
                                    {productData.brand}
                                </Typography>
                                <Typography variant="h4" sx={{ mb: 2, fontWeight: 'bold' }}>
                                    {productData.name}
                                </Typography>
                                <Rating name="read-only" value={4} readOnly />
                                <Typography sx={{ mt: 2 }}>{productData.description}</Typography>
                                <Typography variant="h5" sx={{ my: 2 }}>
                                    Precio: ${productData.price}
                                </Typography>
                            </Grid>
                        </Grid>
                        <Divider sx={styles.ThickDivider}></Divider>
                        <Box sx={{ textAlign: 'left' }}>
                            <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                                Product characteristics
                            </Typography>
                            {renderAdditionalAttributes(productData)}
                            <Divider sx={styles.ThickDivider}></Divider>
                            <Box sx={{ my: 2 }}>
                                <Button
                                    variant="contained"
                                    color="success"
                                    onClick={handleOpenApprovalDialog}
                                    sx={{ mr: 1 }}
                                >
                                    Approve
                                </Button>
                                <Button
                                    variant="outlined"
                                    color="error"
                                    onClick={handleOpenRejectionDialog}
                                >
                                    Reject
                                </Button>
                                <Dialog open={openApprovalDialog} onClose={handleCloseApprovalDialog}>
                                    <DialogTitle>Approve Product</DialogTitle>
                                    <DialogContent>
                                        <TextField
                                            label="Eco-points"
                                            variant="outlined"
                                            type="number"
                                            value={ecoPoints}
                                            onChange={(e) => setEcoPoints(parseInt(e.target.value, 10))}
                                            sx={{ width: '100%', mb: 1 }}
                                        />
                                        <FormControlLabel
                                            control={<Switch checked={ageRestriction} onChange={(e) => setAgeRestriction(e.target.checked)} />}
                                            label="Age Restriction"
                                        />
                                    </DialogContent>
                                    <DialogActions>
                                        <Button onClick={handleCloseApprovalDialog} color="error">
                                            Cancel
                                        </Button>
                                        <Button onClick={handleApprove} color="success">
                                            Confirm
                                        </Button>
                                    </DialogActions>
                                </Dialog>
                                <Dialog open={openRejectionDialog} onClose={handleCloseRejectionDialog}>
                                    <DialogTitle>Reject Product</DialogTitle>
                                    <DialogContent>
                                        <TextField
                                            label="Justification"
                                            variant="outlined"
                                            multiline
                                            rows={4}
                                            value={justification}
                                            onChange={(e) => setJustification(e.target.value)}
                                            sx={{ width: '100%', mb: 1 }}
                                        />
                                    </DialogContent>
                                    <DialogActions>
                                        <Button onClick={handleCloseRejectionDialog} color="error">
                                            Cancel
                                        </Button>
                                        <Button onClick={handleReject} color="success">
                                            Submit
                                        </Button>
                                    </DialogActions>
                                </Dialog>
                            </Box>
                        </Box>
                    </Paper>
                )}
            </Container>
            <Footer />
        </Box>
    );
};

export default ValidateProductPage;
