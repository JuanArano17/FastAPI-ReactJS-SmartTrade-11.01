import React, { useState } from "react";
import { Box, Typography, Button, Container } from "@mui/material";
import TopBar from "../components/topbar/TopBar";
import Footer from "../components/footer/Footer";
import SellerRegistration from "../components/register/SellerRegistration";
import BuyerRegistration from "../components/register/BuyerRegistration";
import img_Buyer from "../images/img_Buyer.png";
import img_Seller from "../images/img_Seller.png";
import img_mundo from "../images/img_mundo.png";
import styles from "../styles/styles.js";
const RegisterPage = () => {
    const [selectedOption, setSelectedOption] = useState(null);
    const handleOptionSelect = (option) => {
        setSelectedOption(option);
    };
    return (
        <Box sx={styles.mainBox}>
            <TopBar showRegisterButton={false} />
            <Container component="main" sx={{ mt: 4, mb: 4, flex: 1 }}>
                {selectedOption === null ? (
                    <>
                        <Typography variant="h4" align="center" color="#629c44" marginTop={"20px"} marginBottom={"20px"}>
                            What are you looking for?
                        </Typography>
                        <Box display="flex" justifyContent="center" alignItems="center" mb={32}>
                            <Box textAlign="center" mr={4} style={{ width: "275px", marginBottom: "10px" }}>
                                <Button
                                    sx={styles.greenRoundedButton}
                                    onClick={() => handleOptionSelect("buyer")}
                                >
                                    Buy Products
                                </Button>
                                <img src={img_Buyer} style={styles.imageStyle} alt="Buyer" />
                            </Box>
                            <Box textAlign="center" style={{ width: "275px", marginBottom: "10px" }}>
                                <Button
                                    sx={styles.greenRoundedButton}
                                    onClick={() => handleOptionSelect("seller")}
                                >
                                    Sell Products
                                </Button>
                                <img src={img_Seller} style={styles.imageStyle} alt="Seller" />
                            </Box>
                        </Box>
                    </>
                ) : (
                    <>
                        <img src={img_mundo} style={styles.rounded_img} />
                        {selectedOption === "buyer" ? (
                            <BuyerRegistration />
                        ) : (
                            <SellerRegistration />
                        )}
                    </>
                )}
            </Container>
            <Footer />
        </Box>
    );
};

export default RegisterPage;
