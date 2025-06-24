"""Tests for CLI module."""

import pytest
import argparse
from unittest.mock import patch, MagicMock
import sys

from genome_matrix_mds.cli import (
    create_parser,
    run_mds_analysis,
    run_dbscan_analysis,
    run_parameter_sweep,
    main
)


class TestCLI:
    """Test CLI functionality."""
    
    def test_create_parser(self):
        """Test parser creation."""
        parser = create_parser()
        
        assert isinstance(parser, argparse.ArgumentParser)
        
        # Test version argument
        with patch('sys.exit'):
            with patch('builtins.print'):
                parser.parse_args(['--version'])
    
    def test_mds_subcommand_parser(self):
        """Test MDS subcommand parsing."""
        parser = create_parser()
        
        args = parser.parse_args([
            'mds', 
            'test_matrix.dist',
            '--output', 'test_output.png',
            '--data-dir', 'test_data'
        ])
        
        assert args.command == 'mds'
        assert args.distance_matrix == 'test_matrix.dist'
        assert args.output == 'test_output.png'
        assert args.data_dir == 'test_data'
    
    def test_dbscan_subcommand_parser(self):
        """Test DBSCAN subcommand parsing."""
        parser = create_parser()
        
        args = parser.parse_args([
            'dbscan',
            'test_matrix.dist',
            '--epsilon', '0.2',
            '--min-samples', '5',
            '--output', 'test_dbscan'
        ])
        
        assert args.command == 'dbscan'
        assert args.distance_matrix == 'test_matrix.dist'
        assert args.epsilon == 0.2
        assert args.min_samples == 5
        assert args.output == 'test_dbscan'
    
    def test_sweep_subcommand_parser(self):
        """Test parameter sweep subcommand parsing."""
        parser = create_parser()
        
        args = parser.parse_args([
            'sweep',
            'test_matrix.dist',
            '--eps-range', '0.1', '0.3', '0.05',
            '--min-samples-range', '3', '8', '1',
            '--output', 'test_sweep'
        ])
        
        assert args.command == 'sweep'
        assert args.distance_matrix == 'test_matrix.dist'
        assert args.eps_range == [0.1, 0.3, 0.05]
        assert args.min_samples_range == [3, 8, 1]
        assert args.output == 'test_sweep'
    
    @patch('genome_matrix_mds.cli.MDSPlotter')
    @patch('genome_matrix_mds.cli.DataLoader')
    @patch('builtins.print')
    def test_run_mds_analysis(self, mock_print, mock_loader_class, mock_plotter_class):
        """Test MDS analysis execution."""
        # Setup mocks
        mock_loader = MagicMock()
        mock_loader_class.return_value = mock_loader
        mock_loader.load_distance_matrix.return_value = (MagicMock(), ['acc1', 'acc2'])
        mock_loader.load_metadata.return_value = MagicMock()
        mock_loader.create_taxonomy_mappings.return_value = {'species': {}}
        mock_loader.prepare_labels.return_value = ['Species_1', 'Species_2']
        
        mock_plotter = MagicMock()
        mock_plotter_class.return_value = mock_plotter
        mock_plotter.run_mds.return_value = [[0, 1], [1, 0]]
        mock_plotter.create_mds_dataframe.return_value = MagicMock()
        mock_plotter.plot_mds_by_species.return_value = MagicMock()
        
        # Create test args
        args = argparse.Namespace(
            distance_matrix='test.dist',
            metadata='test_meta.tsv',
            output='test_out.png',
            data_dir='test_data'
        )
        
        run_mds_analysis(args)
        
        # Verify calls
        mock_loader_class.assert_called_once_with('test_data')
        mock_loader.load_distance_matrix.assert_called_once_with('test.dist')
        mock_plotter.run_mds.assert_called_once()
        mock_print.assert_called_with("MDS plot saved to: test_out.png")
    
    @patch('genome_matrix_mds.cli.DBSCANAnalyzer')
    @patch('genome_matrix_mds.cli.DataLoader')
    @patch('builtins.print')
    def test_run_dbscan_analysis(self, mock_print, mock_loader_class, mock_analyzer_class):
        """Test DBSCAN analysis execution."""
        # Setup mocks
        mock_loader = MagicMock()
        mock_loader_class.return_value = mock_loader
        mock_loader.load_distance_matrix.return_value = (MagicMock(), ['acc1', 'acc2'])
        mock_loader.prepare_labels.return_value = ['Species_1', 'Species_2']
        
        mock_analyzer = MagicMock()
        mock_analyzer_class.return_value = mock_analyzer
        mock_stats = [5, 0.1, 3, 1, 0.8, 0.7, 0.75, 0.6, 0.65]
        mock_analyzer.run_dbscan.return_value = (mock_stats, [0, 0])
        
        # Create test args
        args = argparse.Namespace(
            distance_matrix='test.dist',
            epsilon=0.1,
            min_samples=5,
            metadata=None,
            output='test_dbscan',
            data_dir='test_data'
        )
        
        run_dbscan_analysis(args)
        
        # Verify calls
        mock_analyzer.run_dbscan.assert_called_once()
        mock_analyzer.save_results.assert_called_once()
        
        # Check that results were printed
        assert mock_print.call_count >= 5  # Should print multiple result lines
    
    @patch('genome_matrix_mds.cli.DBSCANAnalyzer')
    @patch('genome_matrix_mds.cli.DataLoader')
    @patch('builtins.print')
    def test_run_parameter_sweep(self, mock_print, mock_loader_class, mock_analyzer_class):
        """Test parameter sweep execution."""
        # Setup mocks
        mock_loader = MagicMock()
        mock_loader_class.return_value = mock_loader
        mock_loader.load_distance_matrix.return_value = (MagicMock(), ['acc1', 'acc2'])
        mock_loader.prepare_labels.return_value = ['Species_1', 'Species_2']
        
        mock_analyzer = MagicMock()
        mock_analyzer_class.return_value = mock_analyzer
        mock_stats_list = [[5, 0.1, 3, 1, 0.8, 0.7, 0.75, 0.6, 0.65]]
        mock_analyzer.run_parameter_sweep.return_value = (mock_stats_list, [[0, 0]])
        mock_analyzer.find_optimal_parameters.return_value = [(0.1, 5)]
        
        # Create test args
        args = argparse.Namespace(
            distance_matrix='test.dist',
            eps_range=[0.1, 0.2, 0.05],
            min_samples_range=[3, 6, 1],
            metadata=None,
            output='test_sweep',
            data_dir='test_data'
        )
        
        run_parameter_sweep(args)
        
        # Verify calls
        mock_analyzer.run_parameter_sweep.assert_called_once()
        mock_analyzer.save_results.assert_called_once()
        mock_analyzer.find_optimal_parameters.assert_called_once()
    
    @patch('genome_matrix_mds.cli.run_mds_analysis')
    def test_main_mds_command(self, mock_run_mds):
        """Test main function with MDS command."""
        main(['mds', 'test.dist'])
        mock_run_mds.assert_called_once()
    
    @patch('genome_matrix_mds.cli.run_dbscan_analysis')
    def test_main_dbscan_command(self, mock_run_dbscan):
        """Test main function with DBSCAN command."""
        main(['dbscan', 'test.dist'])
        mock_run_dbscan.assert_called_once()
    
    @patch('genome_matrix_mds.cli.run_parameter_sweep')
    def test_main_sweep_command(self, mock_run_sweep):
        """Test main function with sweep command."""
        main(['sweep', 'test.dist'])
        mock_run_sweep.assert_called_once()
    
    def test_main_no_command(self):
        """Test main function with no command."""
        with patch('argparse.ArgumentParser.print_help') as mock_help:
            with patch('sys.exit') as mock_exit:
                main([])
                mock_help.assert_called_once()
                mock_exit.assert_called_once_with(1)
    
    def test_main_invalid_command(self):
        """Test main function with invalid command."""
        with patch('argparse.ArgumentParser.print_help') as mock_help:
            with patch('sys.exit') as mock_exit:
                main(['invalid'])
                mock_help.assert_called_once()
                mock_exit.assert_called_once_with(1)
    
    @patch('genome_matrix_mds.cli.DataLoader')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_run_mds_analysis_error_handling(self, mock_print, mock_exit, mock_loader_class):
        """Test error handling in MDS analysis."""
        # Setup mock to raise exception
        mock_loader_class.side_effect = Exception("Test error")
        
        args = argparse.Namespace(
            distance_matrix='test.dist',
            metadata=None,
            output='test_out.png',
            data_dir='test_data'
        )
        
        run_mds_analysis(args)
        
        # Verify error handling
        mock_print.assert_called_with("Error running MDS analysis: Test error", file=sys.stderr)
        mock_exit.assert_called_once_with(1)
    
    @patch('genome_matrix_mds.cli.DataLoader')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_run_dbscan_analysis_error_handling(self, mock_print, mock_exit, mock_loader_class):
        """Test error handling in DBSCAN analysis."""
        # Setup mock to raise exception
        mock_loader_class.side_effect = Exception("Test error")
        
        args = argparse.Namespace(
            distance_matrix='test.dist',
            epsilon=0.1,
            min_samples=5,
            metadata=None,
            output='test_dbscan',
            data_dir='test_data'
        )
        
        run_dbscan_analysis(args)
        
        # Verify error handling
        mock_print.assert_called_with("Error running DBSCAN analysis: Test error", file=sys.stderr)
        mock_exit.assert_called_once_with(1)
    
    @patch('genome_matrix_mds.cli.DataLoader')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_run_parameter_sweep_error_handling(self, mock_print, mock_exit, mock_loader_class):
        """Test error handling in parameter sweep."""
        # Setup mock to raise exception
        mock_loader_class.side_effect = Exception("Test error")
        
        args = argparse.Namespace(
            distance_matrix='test.dist',
            eps_range=[0.1, 0.2, 0.05],
            min_samples_range=[3, 6, 1],
            metadata=None,
            output='test_sweep',
            data_dir='test_data'
        )
        
        run_parameter_sweep(args)
        
        # Verify error handling
        mock_print.assert_called_with("Error running parameter sweep: Test error", file=sys.stderr)
        mock_exit.assert_called_once_with(1)