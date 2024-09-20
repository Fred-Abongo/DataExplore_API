import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import FileUpload from './FileUpload';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';

// Set up mock adapter for Axios
const mock = new MockAdapter(axios);

describe('FileUpload Component', () => {
    afterEach(() => {
        mock.reset();
    });

    test('uploads file and displays success message', async () => {
        mock.onPost('/api/upload').reply(200, { data_id: '12345' });

        render(<FileUpload />);

        const file = new File(['file content'], 'test-file.txt', { type: 'text/plain' });
        const fileInput = screen.getByLabelText(/Choose file/i);
        const uploadButton = screen.getByText(/Upload/i);

        fireEvent.change(fileInput, { target: { files: [file] } });
        fireEvent.click(uploadButton);

        await waitFor(() => {
            expect(screen.getByText(/File uploaded! Data ID: 12345/i)).toBeInTheDocument();
        });
    });

    test('displays error message on upload failure', async () => {
        mock.onPost('/api/upload').reply(500);

        render(<FileUpload />);

        const file = new File(['file content'], 'test-file.txt', { type: 'text/plain' });
        const fileInput = screen.getByLabelText(/Choose file/i);
        const uploadButton = screen.getByText(/Upload/i);

        fireEvent.change(fileInput, { target: { files: [file] } });
        fireEvent.click(uploadButton);

        await waitFor(() => {
            expect(screen.getByText(/Error uploading file/i)).toBeInTheDocument();
        });
    });
});
