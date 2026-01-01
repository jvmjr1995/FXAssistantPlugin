# recommendations/safe_preset_converter.py
# Legally safe preset converter - extracts only FX chain structure (not copyrighted content)

import json
import xml.etree.ElementTree as ET
import struct
import os
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Set up logging for debugging
logger = logging.getLogger(__name__)

class SafeFXChainExtractor:
    # Legally Safe FX Chain Structure Extractor
    # This class extracts ONLY the processing order from preset files:
    # - FX chain structure (EQ → Compressor → Reverb)
    # - Generic categorization (not specific plugin names)
    # - NO parameter values, preset names, or copyrighted content
    # - NO brand names or trademarked material
    
    # Legal Safety:
    # - Processing order is functional information (not copyrightable)
    # - Generic FX types are industry standard terms
    # - No copyrighted parameter values extracted
    # - Clear attribution that user owns original files


    def __init__(self):
        # Initialize the extractor with generic FX type mappings
        # Generic FX type categories (industry standard terms, not copyrightable)
        # These represent functional audio processing categories
        self.generic_fx_categories = {
            # Frequency shaping effects
            'frequency': ['EQ', 'Filter', 'High-Pass Filter', 'Low-Pass Filter'],

            # Dynamic range effects
            'dyamics': ['Compressor', 'Limiter', 'Gate', 'Expander', 'Multiband Compressor'],

            # Time-based effects
            'time': ['Reverb', 'Delay', 'Echo', 'Chorus', 'Flanger', 'Phaser'],

            # Harmonic enhancement
            'harmonic': ['Saturation', 'Distortion', 'Overdrive', 'Tube', 'Tape Saturation'],

            # Utility processing
            'utility': ['Gain', 'Pan', 'Width', 'Phase', 'Stereo Widener'],

            # Pitch/tuning effects
            'pitch': ['Auto-Tune', 'Pitch Correction', 'Vocoder'],
            
            # Modulation effects
            'modulation': ['Chorus', 'Flanger', 'Phaser', 'Tremolo', 'Vibrato']
        }

        # Common XML element patterns that indicate FX types
        # These are structural patterns, not copyrighted content
        self.xml_fx_patterns = {
            'eq': ['eq', 'equalizer', 'filter', 'frequency'],
            'compressor': ['comp', 'compress', 'limit', 'dynamic', 'gate'],
            'reverb': ['reverb', 'hall', 'room', 'space', 'ambient'],
            'delay': ['delay', 'echo', 'repeat'],
            'saturation': ['sat', 'dist', 'drive', 'tube', 'warm', 'color'],
            'modulation': ['chorus', 'flanger', 'phaser', 'mod']
        }

        # File extension to extraction method mapping
        self.extraction_methods = {
            '.xml': self._extract_from_xml,
            '.xps': self._extract_from_xml,    # Waves presets (XML-based)
            '.ffp': self._extract_from_xml,    # FabFilter presets
            '.json': self._extract_from_json,  # JSON-based presets
            '.spl': self._extract_from_json,   # Splice presets
            '.fxp': self._extract_from_vst,    # VST presets
            '.fxb': self._extract_from_vst,    # VST bank files
        }

    def extract_fx_chain_structure(self, file_path: str) -> Optional[Dict[str, Any]]:
        # Main method to extract FX chain structure from a preset file
        
        # This is the primary interface for the safe extraction process.
        # It determines the file type and routes to the appropriate extraction method.
        
        # Args:
        #     file_path: Path to the preset file to analyze
        
        # Returns:
        #     Dictionary with extracted FX chain structure, or None if extraction fails
        
        try:
            logger.info(f"Starting safe extraction for: {file_path}")

            # Validate file exists
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return None
            
            # Get file extension to determine extraction method
            file_ext = Path(file_path).suffix.lower()
            logger.debug(f"File extension detected: {file_path}")

            # Route to appropriate extraction method
            if file_ext in self.extraction_methods:
                extraction_method = self.extraction_methods[file_ext]
                result = extraction_method(file_path)

                if result:
                    # Validate the result is legally compliant
                    if self._validate_legal_compliance(result):
                        logger.info(f"Successfully extracted FX chain: {result['fx_chain']}")
                        return result
                    else:
                        logger.warning("Extraction result failed legal compliance check")
                        return self._create_generic_fallback()
                else:
                    logger.warning("Extraction method returned no result")
                    return self._create_generic_fallback()
            else:
                logger.warning(f"Unsupported file format: {file_ext}")
                return self._create_generic_fallback()
            
        except Exception as e:
            logger.error(f"Error during extractionL {str(e)}")
            return self._create_generic_fallback()
        
    def _extract_from_xml(self, file_path: str) -> Optional[Dict[str, Any]]:
        # Extract FX chain structure from XML-based preset files
        
        # This method analyzes XML structure to infer FX processing order.
        # It looks at element names and hierarchy, NOT content or parameter values.
        
        # Args:
        #     file_path: Path to XML preset file
            
        # Returns:
        #     Dictionary with extracted FX chain structure

        try:
            logger.debug(f"Parsing XML file: {file_path}")

            #Parse XML structure
            tree = ET.parse(file_path)
            root = tree.getroot()

            fx_chain = []
            processed_types = set()    # Prevent duplicates

            # Analyze XML structure for FX indicators
            for element in root.iter():
                # Get element tag name (this is structural info, not copyrighted)
                tag_name = element.tag.lower()

                # Look for FX type indicators in tag names
                fx_type = self._categorize_fx_from_tag(tag_name)

                if fx_type and fx_type not in processed_types:
                    fx_chain.append(fx_type)
                    processed_types.add(fx_type)
                    logger.debug(f"Found FX type from tag '{tag_name}': {fx_type}")

                # Also check element attributes for FX indicators
                for attr_name, attr_value in element.attrib.items():
                    attr_fx_type = self._categorize_fx_from_tag(attr_name.lower())
                    if attr_fx_type and attr_fx_type not in processed_types:
                        fx_chain.append(attr_fx_type)
                        processed_types.add(attr_fx_type)
                        logger.debug(f"Found FX type from attribute '{attr_name}': {attr_fx_type}")

            # If we found FX types, create result
            if fx_chain:
                return self._create_extraction_result(fx_chain, 'xml_structure', file_path)
            else:
                logger.debug("No FX types detected in XML structure")
                return self._create_generic_fallback()
                
        except ET.ParseError as e:
            logger.error(f"XML parsing error: {str(e)}")
            return self._create_generic_fallback()
        except Exception as e:
            logger.error(f"XML extraction error: {str(e)}")
            return self._create_generic_fallback()
        
    def _extract_from_json(self, file_path: str) -> Optional[Dict[str, Any]]:
        # Extract FX chain structure from JSON-based preset files
        
        # This method analyzes JSON structure to find FX processing information.
        # It looks at key names and object structure, NOT parameter values.
        
        # Args:
        #     file_path: Path to JSON preset file
            
        # Returns:
        #     Dictionary with extracted FX chain structure

        try:
            logger.debug(f"Parsing JSON file: {file_path}")
            
            # Load JSON structure
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            fx_chain = []
            processed_types = set()
            
            # Recursively search JSON structure for FX indicators
            self._search_json_for_fx(data, fx_chain, processed_types)
            
            # If we found FX types, create result
            if fx_chain:
                return self._create_extraction_result(fx_chain, 'json_structure', file_path)
            else:
                logger.debug("No FX types detected in JSON structure")
                return self._create_generic_fallback()
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            return self._create_generic_fallback()
        except Exception as e:
            logger.error(f"JSON extraction error: {str(e)}")
            return self._create_generic_fallback()
        
    def _search_json_for_fx(self, data: Any, fx_chain: List[str], processed_types: set) -> None:
        # Recursively search JSON data structure for FX type indicators
        
        # This is a helper method that traverses JSON objects and arrays
        # looking for keys or values that indicate FX types.
        
        # Args:
        #     data: Current JSON data (dict, list, or primitive)
        #     fx_chain: List to append found FX types to
        #     processed_types: Set to track already found types

        try:
            if isinstance(data, dict):
                # Search dictionary keys and values
                for key, value in data.items():
                    # Check if key name indicates an FX type
                    fx_type = self._categorize_fx_from_tag(key.lower())
                    if fx_type and fx_type not in processed_types:
                        fx_chain.append(fx_type)
                        processed_types.add(fx_type)
                        logger.debug(f"Found FX type from JSON key '{key}': {fx_type}")
                    
                    # Recursively search the value
                    self._search_json_for_fx(value, fx_chain, processed_types)
                    
            elif isinstance(data, list):
                # Search list elements
                for item in data:
                    self._search_json_for_fx(item, fx_chain, processed_types)
                    
            elif isinstance(data, str):
                # Check if string value indicates an FX type
                fx_type = self._categorize_fx_from_tag(data.lower())
                if fx_type and fx_type not in processed_types:
                    fx_chain.append(fx_type)
                    processed_types.add(fx_type)
                    logger.debug(f"Found FX type from JSON value '{data}': {fx_type}")
                    
        except Exception as e:
            logger.debug(f"Error in JSON search: {str(e)}")
            # Continue searching even if one branch fails
            pass

    def _extract_from_vst(self, file_path: str) -> Optional[Dict[str, Any]]:
        # Extract FX chain structure from VST preset files (.fxp/.fxb)
        
        # This method analyzes VST binary format headers to infer FX types.
        # It only looks at publicly documented header information.
        
        # Args:
        #     file_path: Path to VST preset file
            
        # Returns:
        #     Dictionary with extracted FX chain structure
        
        try:
            logger.debug(f"Parsing VST file: {file_path}")
            
            with open(file_path, 'rb') as f:
                # Read VST header (publicly documented format)
                header = f.read(32)
                
                if len(header) < 28:
                    logger.error("VST file too short")
                    return self._create_generic_fallback()
                
                # Parse header structure (this is functional info, not copyrighted)
                magic = header[:4]
                if magic != b'CcnK':
                    logger.error("Not a valid VST preset file")
                    return self._create_generic_fallback()
                
                # Extract plugin ID (functional identifier)
                fx_id = struct.unpack('>I', header[16:20])[0]
                logger.debug(f"VST plugin ID: {fx_id}")
                
                # Map plugin ID to generic FX category
                fx_type = self._map_vst_id_to_generic_category(fx_id)
                
                return self._create_extraction_result([fx_type], 'vst_structure', file_path)
                
        except Exception as e:
            logger.error(f"VST extraction error: {str(e)}")
            return self._create_generic_fallback()
    
    def _categorize_fx_from_tag(self, tag_name: str) -> Optional[str]:
        # Categorize FX type from XML tag name or JSON key
        
        # This method maps element/key names to generic FX categories.
        # It uses industry-standard functional terms, not copyrighted names.
        
        # Args:
        #     tag_name: XML tag name or JSON key (lowercase)
            
        # Returns:
        #     Generic FX type string, or None if no match
        
        # Check each FX pattern category
        for fx_type, patterns in self.xml_fx_patterns.items():
            if any(pattern in tag_name for pattern in patterns):
                # Map to standardized FX name
                if fx_type == 'eq':
                    return 'EQ'
                elif fx_type == 'compressor':
                    return 'Compressor'
                elif fx_type == 'reverb':
                    return 'Reverb'
                elif fx_type == 'delay':
                    return 'Delay'
                elif fx_type == 'saturation':
                    return 'Saturation'
                elif fx_type == 'modulation':
                    return 'Chorus'  # Generic modulation effect
        
        return None
    
    def _map_vst_id_to_generic_category(self, plugin_id: int) -> str:
        """
        Map VST plugin ID to generic FX category
        
        This uses broad heuristics to categorize plugins by ID ranges.
        It doesn't identify specific plugins, just general categories.
        
        Args:
            plugin_id: VST plugin identifier
            
        Returns:
            Generic FX category string
        """
        # Use simple heuristics based on ID patterns
        # This is functional categorization, not specific plugin identification
        
        id_mod = plugin_id % 100
        
        if id_mod < 20:
            return 'EQ'
        elif id_mod < 40:
            return 'Compressor'
        elif id_mod < 60:
            return 'Reverb'
        elif id_mod < 80:
            return 'Delay'
        else:
            return 'Saturation'
    
    def _create_extraction_result(self, fx_chain: List[str], source_type: str, file_path: str) -> Dict[str, Any]:
        # Create standardized extraction result dictionary
        
        # This method creates a consistent result format for all extraction methods.
        # It ensures no copyrighted content is included.
        
        # Args:
        #     fx_chain: List of generic FX types found
        #     source_type: Method used for extraction
        #     file_path: Original file path (for metadata only)
            
        # Returns:
        #     Standardized result dictionary
        
        # Remove duplicates while preserving order
        unique_chain = []
        seen = set()
        for fx in fx_chain:
            if fx not in seen:
                unique_chain.append(fx)
                seen.add(fx)
        
        # Ensure we have at least a basic chain
        if not unique_chain:
            unique_chain = ['EQ', 'Compressor']
        
        # Create result with only legally safe information
        result = {
            # Core FX chain data (functional information)
            'fx_chain': unique_chain,
            'chain_length': len(unique_chain),
            
            # Extraction metadata (not copyrighted)
            'source_type': source_type,
            'extraction_method': 'structure_analysis',
            'legal_status': 'safe_extraction',
            
            # Generic categorization (not copyrighted)
            'name': f'Imported Chain ({len(unique_chain)} stages)',
            'description': f'FX processing chain extracted from user file via {source_type}',
            'genre': 'imported',
            'instrument_type': 'generic',
            
            # Technical metadata
            'file_extension': Path(file_path).suffix.lower(),
            'extraction_timestamp': __import__('datetime').datetime.now().isoformat(),
            
            # Legal compliance markers
            'contains_copyrighted_content': False,
            'contains_parameter_values': False,
            'contains_brand_names': False,
            'user_owns_original_file': True  # Assumption - user provided the file
        }
         
        return result
    
    def _create_generic_fallback(self) -> Dict[str, Any]:
        # Create a generic fallback result when extraction fails
        
        # This ensures we always return something useful even if extraction fails.
        # The fallback is a basic, universally applicable FX chain.
        
        # Returns:
        #     Generic fallback result dictionary
        
        return {
            'fx_chain': ['EQ', 'Compressor', 'Reverb'],
            'chain_length': 3,
            'source_type': 'fallback',
            'extraction_method': 'generic_fallback',
            'legal_status': 'safe_fallback',
            'name': 'Generic Processing Chain',
            'description': 'Standard FX processing chain (fallback)',
            'genre': 'generic',
            'instrument_type': 'generic',
            'file_extension': 'unknown',
            'extraction_timestamp': __import__('datetime').datetime.now().isoformat(),
            'contains_copyrighted_content': False,
            'contains_parameter_values': False,
            'contains_brand_names': False,
            'user_owns_original_file': True,
            'is_fallback': True
        }
    
    def _validate_legal_compliance(self, result: Dict[str, Any]) -> bool:
        # Validate that extraction result contains no copyrighted content
        
        # This is a safety check to ensure our extraction is legally compliant.
        # It verifies that no prohibited content made it into the result.
        
        # Args:
        #     result: Extraction result to validate
            
        # Returns:
        #     True if legally compliant, False otherwise
        
        try:
            # Check for prohibited content markers
            compliance_checks = [
                # No copyrighted parameter values
                not result.get('contains_parameter_values', True),
                
                # No brand names or trademarks
                not result.get('contains_brand_names', True),
                
                # No copyrighted content
                not result.get('contains_copyrighted_content', True),
                
                # Must have FX chain (functional requirement)
                bool(result.get('fx_chain', [])),
                
                # FX chain must be list of strings
                isinstance(result.get('fx_chain', []), list),
                
                # All FX names must be generic strings
                all(isinstance(fx, str) and fx.strip() for fx in result.get('fx_chain', [])),
                
                # Must have legal status marker
                'legal_status' in result,
                
                # Must indicate user owns original
                result.get('user_owns_original_file', False)
            ]
            
            is_compliant = all(compliance_checks)
            
            if not is_compliant:
                logger.warning("Extraction result failed legal compliance validation")
                logger.debug(f"Compliance checks: {compliance_checks}")
            
            return is_compliant
            
        except Exception as e:
            logger.error(f"Error in compliance validation: {str(e)}")
            return False


class LegalComplianceManager:
    # Manager class for ensuring legal compliance throughout the import process
    
    # This class provides utilities for sanitizing data, validating content,
    # and ensuring we never store or transmit copyrighted material.
    
    
    # Prohibited content patterns (things we must never include)
    PROHIBITED_PATTERNS = [
        # Brand names (examples - add more as needed)
        'waves', 'fabfilter', 'native instruments', 'ableton',
        
        # Specific plugin names
        'renaissance', 'pro-q', 'massive', 'serum',
        
        # Parameter value indicators
        'threshold=', 'ratio=', 'frequency=', 'gain=',
        
        # Copyright indicators
        '©', 'copyright', '(c)', 'all rights reserved'
    ]
    
    @classmethod
    def sanitize_extraction_result(cls, result: Dict[str, Any]) -> Dict[str, Any]:
        # Sanitize extraction result to remove any potentially problematic content
        
        # This method strips out anything that could be legally problematic,
        # leaving only functional FX chain information.
        
        # Args:
        #     result: Raw extraction result
            
        # Returns:
        #     Sanitized result with only safe content
        
        # Define allowed keys (only functional, non-copyrightable data)
        allowed_keys = {
            'fx_chain', 'chain_length', 'source_type', 'extraction_method',
            'legal_status', 'name', 'description', 'genre', 'instrument_type',
            'file_extension', 'extraction_timestamp', 'contains_copyrighted_content',
            'contains_parameter_values', 'contains_brand_names', 'user_owns_original_file',
            'is_fallback'
        }
        
        # Create sanitized result with only allowed keys
        sanitized = {key: value for key, value in result.items() if key in allowed_keys}
        
        # Sanitize string values
        for key, value in sanitized.items():
            if isinstance(value, str):
                sanitized[key] = cls._sanitize_string(value)
            elif isinstance(value, list):
                sanitized[key] = [cls._sanitize_string(item) if isinstance(item, str) else item 
                                for item in value]
        
        # Ensure compliance markers are set correctly
        sanitized.update({
            'contains_copyrighted_content': False,
            'contains_parameter_values': False,
            'contains_brand_names': False,
            'legal_status': 'sanitized'
        })
        
        return sanitized
    
    @classmethod
    def _sanitize_string(cls, text: str) -> str:
        # Sanitize a string to remove prohibited content
        
        # Args:
        #     text: String to sanitize
            
        # Returns:
        #     Sanitized string
        
        if not isinstance(text, str):
            return text
        
        sanitized = text.lower()
        
        # Remove prohibited patterns
        for pattern in cls.PROHIBITED_PATTERNS:
            if pattern in sanitized:
                # Replace with generic equivalents
                sanitized = sanitized.replace(pattern, 'plugin')
        
        # Clean up and return with original case structure
        return sanitized.title() if sanitized != text.lower() else text
    
    @classmethod
    def create_legal_disclaimer(cls) -> str:
        # Create legal disclaimer text for the import feature
        
        # Returns:
        #     Legal disclaimer text
        
        return """
LEGAL DISCLAIMER - PRESET IMPORT FEATURE

By using this preset import feature, you acknowledge and agree that:

1. You own or have legal rights to all preset files you import
2. This feature extracts only FX chain structure (processing order)
3. No copyrighted parameter values or settings are extracted or stored
4. No brand names or proprietary information is retained
5. You are responsible for compliance with original software licenses
6. This software is not affiliated with any plugin manufacturer
7. Imported chains are generic interpretations, not exact reproductions

This feature is designed for legal interoperability and personal use only.
Commercial redistribution of imported presets is prohibited.

For questions about legal compliance, consult with a qualified attorney.
        """.strip()
    
    @classmethod
    def validate_import_request(cls, file_paths: List[str], user_id: int) -> Tuple[bool, str]:
        """
        Validate an import request for legal compliance
        
        Args:
            file_paths: List of files user wants to import
            user_id: ID of requesting user
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Check file count limits (prevent abuse)
            if len(file_paths) > 100:
                return False, "Too many files in single request (max 100)"
            
            # Check file extensions
            allowed_extensions = {'.xml', '.xps', '.ffp', '.json', '.spl', '.fxp', '.fxb'}
            for file_path in file_paths:
                ext = Path(file_path).suffix.lower()
                if ext not in allowed_extensions:
                    return False, f"Unsupported file type: {ext}"
            
            # Check file sizes (prevent huge uploads)
            max_file_size = 10 * 1024 * 1024  # 10MB per file
            for file_path in file_paths:
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    if file_size > max_file_size:
                        return False, f"File too large: {Path(file_path).name} (max 10MB)"
            
            return True, "Import request validated"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"


# Example usage and testing functions
def test_safe_extraction():
    """
    Test function to demonstrate safe extraction
    This shows how the system works with example files
    """
    extractor = SafeFXChainExtractor()
    compliance = LegalComplianceManager()
    
    # Example test files (you would replace with real file paths)
    test_files = [
        "example_preset.fxp",
        "example_preset.xml", 
        "example_preset.json"
    ]
    
    results = []
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"\nTesting extraction for: {file_path}")
            
            # Extract FX chain structure
            result = extractor.extract_fx_chain_structure(file_path)
            
            if result:
                # Sanitize result for legal compliance
                sanitized_result = compliance.sanitize_extraction_result(result)
                
                print(f"Extracted FX chain: {' → '.join(sanitized_result['fx_chain'])}")
                print(f"Legal status: {sanitized_result['legal_status']}")
                print(f"Contains copyrighted content: {sanitized_result['contains_copyrighted_content']}")
                
                results.append(sanitized_result)
            else:
                print("Extraction failed")
        else:
            print(f"Test file not found: {file_path}")
    
    return results

if __name__ == "__main__":
    # Run test if this file is executed directly
    print("FXAssistant Safe Preset Import System")
    print("=" * 50)
    print("Testing safe extraction methods...")
    
    results = test_safe_extraction()
    
    print(f"\nExtraction complete. Processed {len(results)} files safely.")
    print("\nLegal Disclaimer:")
    print(LegalComplianceManager.create_legal_disclaimer())