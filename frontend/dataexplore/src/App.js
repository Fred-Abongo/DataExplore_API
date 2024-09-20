import React from 'react';
import FileUpload from './components/FileUpload';
import DataFilter from './components/DataFilter';
import ChartVisualization from './components/ChartVisualization';

const App = () => {
    return (
        <div>
            <h1>Welcome to DataExplore</h1>
            {/* File Upload Component */}
            <FileUpload />
            
            {/* Data Filter Component */}
            <DataFilter />
            
            {/* Chart Visualization Component */}
            <ChartVisualization />
        </div>
    );
};

export default App;
