import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import DataFilter from './DataFilter';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';

// Set up mock adapter for Axios
const mock = new MockAdapter(axios);

describe('DataFilter Component', () => {
    afterEach(() => {
        mock.reset();
    });

    test('applies filters and displays data', async () => {
        const mockData = [
            { id: 1, name: 'Item 1', date: '2024-01-01' },
            { id: 2, name: 'Item 2', date: '2024-01-02' },
        ];
        mock.onPost('/api/filter').reply(200, mockData);

        render(<DataFilter />);

        fireEvent.change(screen.getByLabelText(/Start Date/i), { target: { value: '2024-01-01' } });
        fireEvent.change(screen.getByLabelText(/End Date/i), { target: { value: '2024-01-02' } });
        fireEvent.click(screen.getByText(/Apply Filters/i));

        await waitFor(() => {
            expect(screen.getByText(/Item 1/i)).toBeInTheDocument();
            expect(screen.getByText(/Item 2/i)).toBeInTheDocument();
        });
    });

    test('displays error message on filter failure', async () => {
        mock.onPost('/api/filter').reply(500);

        render(<DataFilter />);

        fireEvent.change(screen.getByLabelText(/Start Date/i), { target: { value: '2024-01-01' } });
        fireEvent.change(screen.getByLabelText(/End Date/i), { target: { value: '2024-01-02' } });
        fireEvent.click(screen.getByText(/Apply Filters/i));

        await waitFor(() => {
            expect(screen.getByText(/Error applying filters/i)).toBeInTheDocument();
        });
    });
});
