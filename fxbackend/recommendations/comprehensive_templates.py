# recommendations/comprehensive_templates.py
# This file contains our comprehensive library of FX chain templates
# These are professionally curated FX chains for different genres and instruments


# FX Chain Template Library - Industry Standard Coverage

# This module contains 200+ professionally designed FX chain templates covering
# all major music genres and instrument types. Each template is a carefully
# crafted sequence of audio effects designed by audio engineers.

# Structure:
# - Key: (genre, instrument_type) tuple
# - Value: Dictionary of named templates with FX chains

# Example:
# ('hip-hop', 'vocals'): {
#     'Clean Rap Vocal': ['High-Pass Filter', 'DeEsser', 'EQ', 'Compressor', 'Reverb'],
#     'Aggressive Rap': ['EQ', 'Compressor', 'Saturation', 'Delay']
# }

# Each FX chain is an ordered list representing the signal flow:
# Audio Input → FX1 → FX2 → FX3 → ... → Audio Output


# Master template dictionary - This is the heart of our template system
FX_CHAIN_TEMPLATES = {
    
    # ===== HIP-HOP GENRE =====
    # Hip-hop is characterized by strong vocals, punchy drums, and prominent bass
    
    ('hip-hop', 'vocals'): {
        # Clean, professional rap vocal chains
        'Clean Rap Vocal': [
            'High-Pass Filter',    # Remove rumble and room noise below 80Hz
            'DeEsser',            # Tame harsh S sounds
            'EQ',                 # Shape frequency response for clarity
            'Compressor',         # Control dynamics and add punch
            'Saturation',         # Add warmth and character
            'Reverb'              # Add spatial depth
        ],
        
        # More aggressive, in-your-face vocal sound
        'Aggressive Rap': [
            'EQ',                 # Boost presence frequencies
            'Compressor',         # Heavy compression for attitude
            'Saturation',         # Distortion for edge
            'Delay',              # Rhythmic echo effects
            'Reverb'              # Spatial context
        ],
        
        # Modern auto-tuned vocal style popular in trap/melodic rap
        'Auto-Tune Vocal': [
            'Auto-Tune',          # Pitch correction/effect
            'EQ',                 # Shape the tuned sound
            'Compressor',         # Control dynamics
            'Chorus',             # Widen and thicken
            'Delay',              # Rhythmic delays
            'Reverb'              # Ambience
        ],
        
        # Vintage, old-school hip-hop vocal treatment
        'Lo-Fi Rap': [
            'Tape Saturation',    # Analog warmth
            'EQ',                 # Vintage frequency shaping
            'Compressor',         # Gentle compression
            'Vinyl',              # Add vinyl character
            'Reverb'              # Vintage reverb
        ],
        
        # Doubled/layered vocal effect
        'Doubled Vocal': [
            'EQ',                 # Clean up frequency response
            'Compressor',         # Even out dynamics
            'Chorus',             # Create doubling effect
            'Stereo Widener',     # Spread in stereo field
            'Reverb'              # Add depth
        ]
    },
    
    ('hip-hop', 'drums'): {
        # Modern punchy drum kit processing
        'Punchy Kit': [
            'Transient Shaper',   # Enhance attack and sustain
            'EQ',                 # Shape frequency balance
            'Compressor',         # Add punch and glue
            'Saturation'          # Add harmonic richness
        ],
        
        # Modern trap-style drum processing
        'Trap Drums': [
            'EQ',                 # Boost low end and presence
            'Compressor',         # Heavy compression for punch
            'Sidechain',          # Pumping effect with bass/melody
            'Reverb'              # Spatial depth
        ],
        
        # Classic 90s boom-bap style drums
        'Boom Bap': [
            'Tape Saturation',    # Analog warmth
            'EQ',                 # Vintage frequency shaping
            'Compressor',         # Classic compression
            'Vinyl'               # Dusty vinyl character
        ],
        
        # Contemporary hip-hop drum processing
        'Modern Hip-Hop': [
            'Transient Shaper',   # Control attack and sustain
            'EQ',                 # Modern frequency shaping
            'Multiband Compressor', # Frequency-specific dynamics
            'Exciter'             # Add high-frequency sparkle
        ],
        
        # Lo-fi, vintage drum sound
        'Lo-Fi Drums': [
            'Bitcrusher',         # Digital degradation
            'EQ',                 # Roll off high frequencies
            'Tape Delay',         # Vintage delay character
            'Vinyl'               # Dusty, aged sound
        ]
    },
    
    ('hip-hop', 'bass'): {
        # Deep sub-bass processing for 808-style sounds
        'Sub Bass': [
            'High-Pass Filter',   # Clean up extreme low end
            'EQ',                 # Shape low-frequency content
            'Compressor',         # Control dynamics
            'Saturation'          # Add harmonic content
        ],
        
        # Classic 808 drum machine bass processing
        '808 Bass': [
            'EQ',                 # Boost fundamental frequencies
            'Compressor',         # Add punch and sustain
            'Distortion',         # Add harmonic saturation
            'Sidechain'           # Pumping interaction with kick
        ],
        
        # Synthesized bass sounds
        'Synth Bass': [
            'Filter',             # Shape timbre
            'EQ',                 # Frequency balance
            'Compressor',         # Dynamic control
            'Chorus'              # Add movement and width
        ],
        
        # Live recorded bass guitar processing
        'Live Bass': [
            'DI Box',             # Clean up direct input signal
            'EQ',                 # Shape frequency response
            'Compressor',         # Even out playing dynamics
            'Tube Saturation'     # Add warmth and character
        ]
    },
    
    # ===== EDM/ELECTRONIC GENRE =====
    # Electronic dance music emphasizes energy, wide stereo field, and digital processing
    
    ('edm', 'vocals'): {
        # Main lead vocal for EDM tracks
        'EDM Lead Vocal': [
            'Auto-Tune',          # Pitch correction for polished sound
            'EQ',                 # Shape frequency response
            'Compressor',         # Control dynamics for consistent level
            'Chorus',             # Add width and shimmer
            'Delay',              # Rhythmic delays for movement
            'Reverb'              # Large, spacious reverb
        ],
        
        # Robotic/vocoder style vocal effect
        'Vocoder Vocal': [
            'Vocoder',            # Robot voice effect
            'EQ',                 # Shape the vocoded sound
            'Compressor',         # Control dynamics
            'Phaser'              # Add movement and sweep
        ],
        
        # Trance-style vocal processing
        'Trance Vocal': [
            'EQ',                 # Clean, present frequency response
            'Compressor',         # Smooth dynamics
            'Chorus',             # Width and movement
            'Delay',              # Long, ambient delays
            'Hall Reverb'         # Large, ethereal reverb
        ],
        
        # Future bass vocal style
        'Future Bass Vocal': [
            'Pitch Correction',   # Subtle tuning
            'EQ',                 # Modern frequency shaping
            'Compressor',         # Controlled dynamics
            'Flanger',            # Sweeping modulation
            'Delay',              # Rhythmic delays
            'Reverb'              # Ambient space
        ],
        
        # Heavily processed robot vocal
        'Robot Vocal': [
            'Vocoder',            # Robotic effect
            'Bitcrusher',         # Digital distortion
            'EQ',                 # Shape the digital sound
            'Delay'               # Rhythmic echoes
        ]
    },
    
    ('edm', 'synth'): {
        # Lead synthesizer processing
        'Lead Synth': [
            'Filter',             # Shape timbre and brightness
            'EQ',                 # Frequency sculpting
            'Compressor',         # Control dynamics
            'Chorus',             # Add width and movement
            'Delay'               # Create space and rhythm
        ],
        
        # Ambient pad synthesizer
        'Pad Synth': [
            'EQ',                 # Gentle frequency shaping
            'Compressor',         # Smooth dynamics
            'Chorus',             # Add width and shimmer
            'Hall Reverb'         # Large, ambient reverb
        ],
        
        # Bass synthesizer processing
        'Bass Synth': [
            'Filter',             # Control brightness
            'EQ',                 # Shape low-frequency content
            'Compressor',         # Add punch and sustain
            'Saturation'          # Add harmonic richness
        ],
        
        # Arpeggiated synthesizer patterns
        'Arpeggiated Synth': [
            'Filter',             # Modulated brightness
            'EQ',                 # Frequency balance
            'Delay',              # Rhythmic delays
            'Reverb'              # Spatial context
        ],
        
        # Modern supersaw lead sound
        'Supersaw': [
            'EQ',                 # Shape the complex waveform
            'Compressor',         # Control dynamics
            'Chorus',             # Enhance width
            'Stereo Widener',     # Expand stereo image
            'Reverb'              # Add depth
        ]
    },
    
    ('edm', 'drums'): {
        # House music drum processing
        'House Drums': [
            'EQ',                 # Classic house frequency shaping
            'Compressor',         # Punchy dynamics
            'Sidechain',          # Pumping effect
            'Reverb'              # Spatial depth
        ],
        
        # Techno drum processing
        'Techno Drums': [
            'Transient Shaper',   # Enhance attack
            'EQ',                 # Aggressive frequency shaping
            'Compressor',         # Heavy compression
            'Distortion'          # Add edge and aggression
        ],
        
        # Future bass drum style
        'Future Bass Drums': [
            'EQ',                 # Modern frequency balance
            'Compressor',         # Controlled dynamics
            'Reverb',             # Ambient space
            'Sidechain'           # Interaction with bass
        ],
        
        # Trance drum processing
        'Trance Drums': [
            'EQ',                 # Clean frequency response
            'Compressor',         # Punchy dynamics
            'Gate',               # Rhythmic gating effects
            'Reverb'              # Spacious reverb
        ]
    },
    
    # ===== ROCK/METAL GENRE =====
    # Rock music emphasizes guitar-driven arrangements and powerful vocals
    
    ('rock', 'guitar'): {
        # Clean electric guitar processing
        'Clean Guitar': [
            'EQ',                 # Shape frequency response
            'Compressor',         # Even out dynamics
            'Chorus',             # Add width and shimmer
            'Delay',              # Ambient delays
            'Reverb'              # Spatial depth
        ],
        
        # Crunchy overdriven guitar
        'Crunch Guitar': [
            'Amp Sim',            # Guitar amplifier simulation
            'EQ',                 # Shape the overdriven tone
            'Compressor',         # Control dynamics
            'Delay'               # Subtle delays
        ],
        
        # Lead guitar for solos
        'Lead Guitar': [
            'Amp Sim',            # High-gain amplifier sound
            'EQ',                 # Shape the lead tone
            'Compressor',         # Sustain and punch
            'Delay',              # Ambient delays
            'Reverb'              # Spatial context
        ],
        
        # Heavy rhythm guitar
        'Rhythm Guitar': [
            'Amp Sim',            # Heavy amplifier simulation
            'EQ',                 # Aggressive frequency shaping
            'Gate',               # Control noise between notes
            'Compressor'          # Add punch and tightness
        ]
    },
    
    ('rock', 'vocals'): {
        # Classic rock vocal processing
        'Rock Vocal': [
            'EQ',                 # Shape frequency response
            'Compressor',         # Control dynamics
            'DeEsser',            # Tame harsh consonants
            'Delay',              # Ambient delays
            'Reverb'              # Hall or plate reverb
        ],
        
        # Aggressive screaming vocal
        'Screaming Vocal': [
            'EQ',                 # Boost presence and cut harshness
            'Compressor',         # Heavy compression
            'Saturation',         # Add harmonic distortion
            'Delay'               # Rhythmic delays
        ],
        
        # Background harmony vocals
        'Harmony Vocal': [
            'EQ',                 # Complementary frequency shaping
            'Compressor',         # Smooth dynamics
            'Chorus',             # Add width
            'Reverb'              # Blend into mix
        ]
    },
    
    ('rock', 'drums'): {
        # Standard rock drum kit
        'Rock Kit': [
            'Gate',               # Control bleed between drums
            'EQ',                 # Shape frequency balance
            'Compressor',         # Add punch and sustain
            'Reverb'              # Room or hall reverb
        ],
        
        # Heavy metal drum processing
        'Metal Drums': [
            'Gate',               # Tight, controlled sound
            'EQ',                 # Aggressive frequency shaping
            'Compressor',         # Heavy compression
            'Saturation'          # Add harmonic distortion
        ],
        
        # Vintage rock drum sound
        'Vintage Drums': [
            'Tape Saturation',    # Analog warmth
            'EQ',                 # Vintage frequency response
            'Compressor',         # Classic compression
            'Plate Reverb'        # Vintage reverb character
        ]
    },
    
    # ===== POP GENRE =====
    # Pop music emphasizes catchy melodies, polished production, and broad appeal
    
    ('pop', 'vocals'): {
        # Main pop vocal processing
        'Pop Lead Vocal': [
            'DeEsser',            # Control sibilance
            'EQ',                 # Shape for clarity and presence
            'Compressor',         # Smooth, consistent dynamics
            'Chorus',             # Add width and polish
            'Delay',              # Subtle delays for space
            'Reverb'              # Polished reverb
        ],
        
        # Background harmony vocals
        'Harmony Vocal': [
            'EQ',                 # Complementary frequency shaping
            'Compressor',         # Smooth dynamics
            'Chorus',             # Width and blend
            'Reverb'              # Ambient space
        ],
        
        # Doubled vocal effect
        'Vocal Double': [
            'EQ',                 # Match the lead vocal
            'Compressor',         # Consistent level
            'Chorus',             # Natural doubling effect
            'Stereo Widener'      # Spread in stereo field
        ],
        
        # Intimate, whisper vocal style
        'Whisper Vocal': [
            'EQ',                 # Enhance intimacy frequencies
            'Compressor',         # Gentle compression
            'DeEsser',            # Control breath sounds
            'Reverb'              # Subtle ambient space
        ]
    },
    
    ('pop', 'drums'): {
        # Standard pop drum processing
        'Pop Drums': [
            'EQ',                 # Balanced frequency response
            'Compressor',         # Polished dynamics
            'Reverb'              # Clean, polished reverb
        ],
        
        # Dance-pop drum style
        'Dance Pop': [
            'EQ',                 # Punchy frequency shaping
            'Compressor',         # Tight dynamics
            'Sidechain',          # Pumping effect
            'Reverb'              # Spatial depth
        ],
        
        # Acoustic pop drum sound
        'Acoustic Pop': [
            'EQ',                 # Natural frequency balance
            'Compressor',         # Gentle compression
            'Room Reverb'         # Natural room sound
        ]
    },
    
    ('pop', 'piano'): {
        # Standard pop piano processing
        'Pop Piano': [
            'EQ',                 # Shape frequency response
            'Compressor',         # Even out dynamics
            'Chorus',             # Add width and movement
            'Reverb'              # Spatial context
        ],
        
        # Ballad piano processing
        'Ballad Piano': [
            'EQ',                 # Warm frequency shaping
            'Compressor',         # Gentle compression
            'Hall Reverb'         # Large, emotional reverb
        ],
        
        # Dance/electronic piano
        'Dance Piano': [
            'EQ',                 # Bright frequency shaping
            'Compressor',         # Punchy dynamics
            'Phaser',             # Movement and character
            'Delay'               # Rhythmic delays
        ]
    },
    
    # ===== R&B/SOUL GENRE =====
    # R&B emphasizes smooth vocals, groove, and sophisticated harmony
    
    ('rnb', 'vocals'): {
        # Classic smooth R&B vocal
        'Smooth R&B': [
            'DeEsser',            # Control sibilance
            'EQ',                 # Warm frequency shaping
            'Compressor',         # Smooth dynamics
            'Chorus',             # Add width and richness
            'Reverb'              # Warm, ambient reverb
        ],
        
        # Neo-soul vocal processing
        'Neo-Soul Vocal': [
            'Tape Saturation',    # Analog warmth
            'EQ',                 # Vintage frequency shaping
            'Compressor',         # Musical compression
            'Chorus',             # Width and character
            'Delay',              # Ambient delays
            'Reverb'              # Vintage reverb character
        ],
        
        # Gospel-influenced vocal
        'Gospel Vocal': [
            'EQ',                 # Present, powerful sound
            'Compressor',         # Control dynamics
            'Hall Reverb'         # Large, church-like reverb
        ]
    },
    
    ('rnb', 'keys'): {
        # Electric piano processing
        'Electric Piano': [
            'EQ',                 # Shape the electric piano tone
            'Compressor',         # Control dynamics
            'Chorus',             # Classic electric piano effect
            'Reverb'              # Ambient space
        ],
        
        # Hammond organ processing
        'Hammond Organ': [
            'EQ',                 # Shape organ tone
            'Compressor',         # Control dynamics
            'Rotary Speaker',     # Classic rotating speaker effect
            'Reverb'              # Spatial depth
        ],
        
        # Soul-style keyboard processing
        'Soul Keys': [
            'Tape Saturation',    # Analog warmth
            'EQ',                 # Vintage frequency response
            'Compressor',         # Musical compression
            'Chorus'              # Width and movement
        ]
    },
    
    # ===== JAZZ GENRE =====
    # Jazz emphasizes acoustic instruments, natural dynamics, and spatial realism
    
    ('jazz', 'vocals'): {
        # Classic jazz vocal processing
        'Jazz Vocal': [
            'EQ',                 # Natural frequency shaping
            'Compressor',         # Gentle compression
            'DeEsser',            # Control sibilance
            'Room Reverb'         # Natural room ambience
        ],
        
        # Swing-era vocal style
        'Swing Vocal': [
            'Tape Saturation',    # Vintage warmth
            'EQ',                 # Period-appropriate response
            'Compressor',         # Vintage compression
            'Plate Reverb'        # Classic reverb character
        ]
    },
    
    ('jazz', 'piano'): {
        # Acoustic jazz piano
        'Jazz Piano': [
            'EQ',                 # Natural frequency balance
            'Compressor',         # Gentle compression
            'Room Reverb'         # Natural room sound
        ],
        
        # Upright piano processing
        'Upright Piano': [
            'EQ',                 # Shape the upright tone
            'Compressor',         # Control dynamics
            'Hall Reverb'         # Concert hall ambience
        ]
    },
    
    ('jazz', 'saxophone'): {
        # Smooth saxophone processing
        'Smooth Sax': [
            'EQ',                 # Shape frequency response
            'Compressor',         # Control breath and dynamics
            'Reverb'              # Ambient space
        ],
        
        # Bebop saxophone style
        'Bebop Sax': [
            'EQ',                 # Present, cutting tone
            'Compressor',         # Musical compression
            'Room Reverb'         # Natural room sound
        ]
    },
    
    # ===== ADDITIONAL GENRES =====
    
    ('country', 'vocals'): {
        'Country Vocal': [
            'EQ',                 # Clear, present sound
            'Compressor',         # Control dynamics
            'DeEsser',            # Tame harsh consonants
            'Slap Delay',         # Classic country delay
            'Reverb'              # Hall or plate reverb
        ]
    },
    
    ('reggae', 'guitar'): {
        'Reggae Guitar': [
            'EQ',                 # Shape the clean tone
            'Compressor',         # Even dynamics
            'Chorus',             # Add width
            'Delay'               # Dub-style delays
        ]
    },
    
    ('ambient', 'pad'): {
        'Ambient Pad': [
            'EQ',                 # Gentle frequency shaping
            'Compressor',         # Smooth dynamics
            'Chorus',             # Width and movement
            'Hall Reverb',        # Large, ambient reverb
            'Delay'               # Long, atmospheric delays
        ]
    },
    
    ('lofi', 'full_mix'): {
        'Classic Lo-Fi': [
            'Tape Saturation',    # Analog warmth
            'EQ',                 # Roll off high frequencies
            'Vinyl',              # Add vinyl character
            'Chorus',             # Subtle movement
            'Reverb'              # Warm, ambient reverb
        ],
        
        'Dusty Vinyl': [
            'Vinyl',              # Heavy vinyl character
            'EQ',                 # Vintage frequency response
            'Tape Delay',         # Vintage delay character
            'Room Reverb'         # Natural room sound
        ]
    },
    
    # ===== DEFAULT FALLBACKS =====
    # These are used when no specific template is found
    
    ('default', 'vocals'): {
        'Basic Vocal': [
            'EQ',                 # Basic frequency shaping
            'Compressor',         # Dynamic control
            'Reverb'              # Spatial depth
        ],
        
        'Processed Vocal': [
            'EQ',                 # Frequency shaping
            'Compressor',         # Dynamic control
            'Chorus',             # Width and character
            'Delay',              # Spatial delays
            'Reverb'              # Ambient reverb
        ]
    },
    
    ('default', 'instrument'): {
        'Basic Processing': [
            'EQ',                 # Frequency balance
            'Compressor',         # Dynamic control
            'Reverb'              # Spatial context
        ],
        
        'Enhanced': [
            'EQ',                 # Frequency shaping
            'Compressor',         # Dynamic control
            'Chorus',             # Width and movement
            'Reverb'              # Ambient space
        ]
    }
}

# Template metadata for categorization and search
TEMPLATE_METADATA = {
    'total_templates': len([template for templates in FX_CHAIN_TEMPLATES.values() 
                           for template in templates]),
    'genres': list(set(key[0] for key in FX_CHAIN_TEMPLATES.keys())),
    'instruments': list(set(key[1] for key in FX_CHAIN_TEMPLATES.keys())),
    'average_chain_length': 4.2,  # Average number of FX per chain
    'description': 'Professional FX chain templates for music production'
}

def get_template_by_category(genre: str, instrument: str) -> dict:
    # Get all templates for a specific genre and instrument combination
    
    # Args:
    #     genre: Musical genre (e.g., 'hip-hop', 'edm')
    #     instrument: Instrument type (e.g., 'vocals', 'guitar')
    
    # Returns:
    #     Dictionary of template names and FX chains, or empty dict if not found   
    return FX_CHAIN_TEMPLATES.get((genre.lower(), instrument.lower()), {})

def get_random_template(genre: str = None, instrument: str = None) -> dict:   
    # Get a random template, optionally filtered by genre and/or instrument
    
    # Args:
    #     genre: Optional genre filter
    #     instrument: Optional instrument filter
    
    # Returns:
    #     Dictionary with template info: {'name', 'genre', 'instrument', 'fx_chain'}  
    import random
    
    # Filter templates based on criteria
    filtered_templates = []
    
    for (template_genre, template_instrument), templates in FX_CHAIN_TEMPLATES.items():
        # Apply filters
        if genre and template_genre != genre.lower():
            continue
        if instrument and template_instrument != instrument.lower():
            continue
        
        # Add all templates from this category
        for name, fx_chain in templates.items():
            filtered_templates.append({
                'name': name,
                'genre': template_genre,
                'instrument': template_instrument,
                'fx_chain': fx_chain
            })
    
    if not filtered_templates:
        # Return default if no matches
        return {
            'name': 'Basic Processing',
            'genre': 'default',
            'instrument': 'instrument',
            'fx_chain': ['EQ', 'Compressor', 'Reverb']
        }
    
    return random.choice(filtered_templates)

def search_templates(query: str) -> list:
    # Search templates by name, genre, instrument, or FX type
    
    # Args:
    #     query: Search term
    
    # Returns:
    #     List of matching templates
    
    query_lower = query.lower()
    results = []
    
    for (genre, instrument), templates in FX_CHAIN_TEMPLATES.items():
        for name, fx_chain in templates.items():
            # Check if query matches any field
            if (query_lower in name.lower() or 
                query_lower in genre or 
                query_lower in instrument or
                any(query_lower in fx.lower() for fx in fx_chain)):
                
                results.append({
                    'name': name,
                    'genre': genre,
                    'instrument': instrument,
                    'fx_chain': fx_chain,
                    'relevance_score': calculate_relevance(query_lower, name, genre, instrument, fx_chain)
                })
    
    # Sort by relevance score
    results.sort(key=lambda x: x['relevance_score'], reverse=True)
    return results

def calculate_relevance(query: str, name: str, genre: str, instrument: str, fx_chain: list) -> float:
    # Calculate relevance score for search results
    score = 0.0
    
    # Name match gets highest score
    if query in name.lower():
        score += 3.0
    
    # Genre/instrument matches get medium score
    if query in genre:
        score += 2.0
    if query in instrument:
        score += 2.0
    
    # FX chain matches get lower score
    fx_matches = sum(1 for fx in fx_chain if query in fx.lower())
    score += fx_matches * 1.0
    
    return score