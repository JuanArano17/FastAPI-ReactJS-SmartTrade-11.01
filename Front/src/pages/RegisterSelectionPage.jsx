import React from "react";
import { Box, Typography, Button } from "@mui/material";
import TopBar from "../components/TopBar/TopBar";
import Footer from "../components/Footer/Footer";
import { Link } from "react-router-dom";
import img_Buyer from "../images/img_Buyer.png";
import img_Seller from "../images/img_Seller.png";
import styles from "../styles/styles.js";


const SelectionPage = () => {
  return (
    <Box>
      <TopBar />
      <Typography variant="h4" align="center" color="#629c44" marginTop={"20px"} marginBottom={"20px"}>
        ¿Qué harás en SmartTrade?
      </Typography>
      <Box display="flex" justifyContent="center" alignItems="center" mb={4}>
        <Box textAlign="center" mr={4} style={{ width: "275px", marginBottom: "10px" }}>
          <Button
          sx={styles.greenRoundedButton} component={Link} to="/registerBuyer"
          >
            VER LA TIENDA
          </Button>
          <img src={img_Buyer} style={styles.imageStyle} />
        </Box>
        <Box textAlign="center" style={{ width: "275px", marginBottom: "10px" }}>
          <Button
          sx={styles.greenRoundedButton} component={Link} to="/registerSeller"
          >
            VENDER PRODUCTOS
          </Button>
          <img src={img_Seller} style={styles.imageStyle} />
        </Box>
      </Box>
      <Footer />
    </Box>
  );
};

export default SelectionPage;
