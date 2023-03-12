import React, {useState} from 'react';
import {Button, Container, TextField, Typography, Grid} from '@mui/material';
import Box from "@mui/material/Box";
import AddAPhotoIcon from '@mui/icons-material/AddAPhoto';
import "../src/App.css";

const images = [
    {
        url: "https://images.unsplash.com/photo-1551963831-b3b1ca40c98e"
    },
    {
        url: "https://images.unsplash.com/photo-1551782450-a2132b4ba21d"
    },
];

const Upload = () => {
    const [file, setFile] = useState(null);
    const [imageURL, setImageURL] = useState(null);
    const [newImages, setNewImages] = useState([]);

    const handleChange = (e) => {
        console.log(e.target.files[0]);
        let file = e.target.files[0];
        setFile(e.target.files[0]);
        setImageURL(URL.createObjectURL(file));
    };

    const handleClick = (e) => {
        setNewImages(images);
    }

    return (
        <Container fixed>
            <Box>
                <Typography variant="h4">
                    Emo Face
                </Typography>
                <Box sx={{height: 600, width: 900, border: 1}}>
                    {
                        imageURL &&
                        <img src={imageURL} alt="images gallery" loading="lazy" className={"upload_img"}/>
                    }
                </Box>
                <Button variant="contained" component="label" startIcon={<AddAPhotoIcon />}>
                    Upload An Image
                    <input hidden accept="image/*" type="file" onChange={handleChange} />
                </Button>

                <Typography variant="body" component="div">
                    Simply describe the new image with what kind of emoji to replace with your face.
                </Typography>
                <Grid container spacing={2}>
                    <Grid item xs={8}>
                        <TextField fullWidth id="outlined-basic" label="Description of the image" variant="outlined" />
                    </Grid>
                    <Grid item xs={4}>
                        <Button variant="contained" onClick={handleClick}>Generate!</Button>
                    </Grid>

                </Grid>

                {
                    newImages.length !== 0 &&
                    <Box>
                        <Typography variant="h5" component="div">
                            Generated Images Result
                        </Typography>
                        <Grid container spacing={2} sx={{width: 800}}>
                            {images.map((file, index) => (
                                <Grid item xs={4} key={index}>
                                    <img src={file.url} alt="images gallery" loading="lazy" className={"new_img"} />
                                </Grid>
                            ))}
                        </Grid>
                    </Box>
                }
            </Box>
        </Container>
    );
};

export default Upload;