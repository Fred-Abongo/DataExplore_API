import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChartVisualization from './ChartVisualization';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import Plot from 'react-plotly.js';

// Set up mock adapter for Axios
const mock = new MockAdapter(axios);

jest.mock('react-plotly.js', () => ({ data, layout }) => (
    <div>
        <h3>Chart</h3>
        <div>{data ? 'Chart Data Rendered' : 'No Data'}</div>
    </div>
));

describe('ChartVisualization Component', () => {
    afterEach(() => {
        mock.reset();
    });

    test('fetches and displays chart data', async () => {
        const mockData = { data: [{ x: [1, 2, 3], y: [4, 5, 6], type: 'scatter' }], layout: {} };
        mock.onPost('/api/visualize').reply(200, mockData);

        render(<ChartVisualization />);

        fireEvent.change(screen.getByLabelText(/Select Chart Type/i), { target: { value: 'scatter' } });

        await waitFor(() => {
            expect(screen.getByText(/Chart Data Rendered/i)).toBeInTheDocument();
        });
    });

    test('displays error message on chart data fetch failure', async () => {
        mock.onPost('/api/visualize').reply(500);

        render(<ChartVisualization />);

        fireEvent.change(screen.getByLabelText(/Select Chart Type/i), { target: { value: 'scatter' } });

        await waitFor(() => {
            expect(screen.getByText(/Error fetching chart data/i)).toBeInTheDocument();
        });
    });
});
