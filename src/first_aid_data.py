# GuardianSOS Offline First Aid Reference Dataset

FIRST_AID_GUIDES = {
    "BLEEDING": {
        "title": "🩸 Heavy Bleeding / Hemorrhage Control",
        "priority": "IMMEDIATE ACTION REQUIRED",
        "steps": [
            "**Apply Direct Pressure**: Place a clean cloth, bandage, or your gloved hand directly over the wound. Press firmly.",
            "**Elevate the Limb**: If the wound is on a limb, raise it above heart level while maintaining pressure to slow flow.",
            "**Tourniquet (Last Resort for Extremities)**: If bleeding is life-threatening and pressure fails, apply a tourniquet 2-3 inches above the wound. *Write down the application time!*",
            "**Keep Warm**: Cover the patient with a blanket to prevent shock and hypothermia.",
            "**Do NOT Remove Soaked Cloths**: If blood seeps through, add more layers on top. Removing them disrupts forming clots."
        ],
        "warnings": [
            "Do NOT pull out any deeply embedded objects. Stabilize them in place with bulky padding."
        ]
    },
    "CARDIAC_ARREST": {
        "title": "🫀 Unresponsiveness & CPR (No Breathing)",
        "priority": "CRITICAL - GOLDEN RESUSCITATION WINDOW",
        "steps": [
            "**Check Response**: Shake the patient's shoulders and shout, 'Are you okay?'. Check for breathing (<10 seconds).",
            "**Call & Alert**: Actively scream for an Automated External Defibrillator (AED) and call 112.",
            "**Start Chest Compressions**: Place the heel of one hand in the center of the chest. Interlock your other hand on top. Push hard and fast at **100 to 120 compressions per minute** (to the beat of 'Staying Alive').",
            "**Compression Depth**: Push down at least 2 inches (5cm) but no more than 2.4 inches.",
            "**Rescue Breaths (If trained)**: Give 2 rescue breaths after every 30 compressions. If untrained, perform **Hands-Only CPR** continuously."
        ],
        "warnings": [
            "Do NOT pause compressions for more than 10 seconds. Continuous blood flow to the brain is vital."
        ]
    },
    "FRACTURES": {
        "title": "🦴 Bone Fractures & Limb Trauma",
        "priority": "STABILIZATION & PAIN MITIGATION",
        "steps": [
            "**Stop Bleeding First**: Treat any open wounds with sterile dressings before addressing the fracture.",
            "**Immobilize the Area**: Do NOT try to realign the bone. Use splints (cardboard, thick rolled newspapers, wood blocks) to secure the joints above and below the injury.",
            "**Apply Cold Packs**: Wrap ice in a towel and apply to reduce swelling and ease intense pain.",
            "**Check Circulation**: Ensure the skin below the splint is warm and has a pulse. If it turns blue or numb, loosen the splint immediately.",
            "**Prevent Shock**: Keep the patient lying flat with their feet elevated slightly (about 12 inches) if no spinal injury is suspected."
        ],
        "warnings": [
            "Do NOT force a protruding bone back into the skin. Keep it clean and dry, splinting around it."
        ]
    },
    "SPINAL_INJURY": {
        "title": "🧠 Neck, Head, or Spine Trauma (High-Speed Collisions)",
        "priority": "PRESERVE LIFE & PREVENT PARALYSIS",
        "steps": [
            "**Minimize Movement**: Keep the patient's head, neck, and spine aligned. Hands-on hold the head on both sides to prevent any tilting.",
            "**Do NOT Move the Patient**: Unless there is an immediate, deadly hazard (e.g., car fire or explosion risk).",
            "**Log-Roll (If vomiting)**: If the patient starts choking on blood or vomit, have 2-3 people roll the body as a single unit, keeping the neck aligned, to clear the airway.",
            "**Keep Helmet On**: Do NOT remove a motorcycle helmet unless the airway is fully blocked and CPR is impossible."
        ],
        "warnings": [
            "Never bend or twist the neck. Even a minor neck flex can cause permanent spinal cord injury."
        ]
    },
    "BURNS": {
        "title": "🔥 Thermal Burns & Explosion Injuries",
        "priority": "COOL & COVER",
        "steps": [
            "**Cool the Burn**: Run cool, clean water over the burn for at least 10 minutes. Do NOT use ice, butter, or ointments.",
            "**Remove Restrictive Items**: Gently take off rings, watches, or tight clothing near the burn before swelling begins.",
            "**Cover Loosely**: Use a sterile, non-stick bandage or clean plastic wrap. Do NOT wrap tightly.",
            "**Treat for Shock**: Lay the patient flat, keep them warm, and elevate legs."
        ],
        "warnings": [
            "Do NOT pop any blisters. Popping them open introduces severe infection risks."
        ]
    }
}

def get_first_aid_guideline(accident_keywords):
    """
    Scans crash reports and returns corresponding first aid instructions.
    Useful for offline, zero-network instant support.
    """
    text = accident_keywords.upper()
    
    if any(k in text for k in ["BLEED", "BLOOD", "CUT", "HEMORRHAGE", "WOUND", "INJURY"]):
        return FIRST_AID_GUIDES["BLEEDING"]
    elif any(k in text for k in ["CPR", "BREATH", "UNRESPONSIVE", "HEART", "PULSE", "CARDIAC"]):
        return FIRST_AID_GUIDES["CARDIAC_ARREST"]
    elif any(k in text for k in ["SPINE", "NECK", "BACK", "HEAD", "BRAIN", "ROLLOVER", "MOTORCYCLE"]):
        return FIRST_AID_GUIDES["SPINAL_INJURY"]
    elif any(k in text for k in ["BONE", "FRACTURE", "ARM", "LEG", "JOINT", "SPLINT"]):
        return FIRST_AID_GUIDES["FRACTURES"]
    elif any(k in text for k in ["BURN", "FIRE", "EXPLOSION", "HEAT", "SMOKE"]):
        return FIRST_AID_GUIDES["BURNS"]
    
    # Default fallback
    return {
        "title": "🩹 General First Aid Response Guidelines",
        "priority": "SAFETY & STABILIZATION",
        "steps": [
            "**Secure the Scene**: Park your vehicle safely, turn on hazard lights, and ensure you won't be hit by passing traffic.",
            "**Do NOT Move Victims**: Keep injured victims stable. Only move them if they are in immediate danger of fire or explosion.",
            "**Establish Airway**: Ensure the victim's airway is clear. Tilt the head back gently if no neck injury is suspected.",
            "**Apply Pressure**: Stop active bleeding by applying direct pressure with clean fabrics.",
            "**Stay with the Patient**: Reassure them, keep them warm, and wait for emergency services to arrive."
        ],
        "warnings": [
            "Always prioritize your own safety first before entering a crash scene."
        ]
    }
