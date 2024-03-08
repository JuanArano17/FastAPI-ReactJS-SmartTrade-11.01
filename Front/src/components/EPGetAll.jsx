import React, { useState } from 'react';
import Button from '@mui/material/Button';
import axios from 'axios';
import { Container, Paper, Card, CardContent, Typography } from '@mui/material';


const EPGetAll = () => {
    const [items, setItems] = useState([]);

    const fetchItems = async () => {
        try {
            const response = await axios.get('http://localhost:3001/items/all/');
            setItems(Object.values(response.data));
        } catch (error) {
            console.error('There was an error fetching the items:', error);
        }
    };

    return (
        <div>
            <Container maxWidth={"sm"}>
                <Paper elevation={12} style={{ padding: '20px', marginTop: '20px' }}>
                    <Button variant="contained" color="primary" onClick={fetchItems}>
                        Get All Items
                    </Button>
                    {items.map((item, index) => (
                        <Card key={index} style={{ marginBottom: '20px' }}>
                            <CardContent>
                                <Typography variant="h5" component="div">
                                    {item.name}
                                </Typography>
                                <Typography sx={{ mb: 1.5 }} color="text.secondary">
                                    {item.provider_name}
                                </Typography>
                                <Typography variant="body2">
                                    {item.description}
                                </Typography>
                                <Typography variant="body1" style={{ marginTop: '10px' }}>
                                    Price: ${item.price}
                                </Typography>
                            </CardContent>
                        </Card>
                    ))}
                </Paper>
            </Container>
        </div>
    );
};

export default EPGetAll;