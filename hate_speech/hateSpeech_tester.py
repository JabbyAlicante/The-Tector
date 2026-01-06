import sys
sys.path.append('hate_speech')
from main import analyze_content

print("=" * 60)
print("HATE SPEECH DETECTOR (Type 'exit' to quit)")
print("=" * 60)

while True:
    msg = input("\nEnter a message to analyze: ").strip()
    
    if msg.lower() == "exit":
        print("Exiting detector. Goodbye!")
        break
    
    if not msg:
        print("⚠️  Please enter a non-empty message.")
        continue

    result = analyze_content(msg)
    print(f"\nSeverity: {result['severity']}")
    
    if result['profanity']['detected']:
        print(f"  ⚠️  Profanity detected: {result['profanity']['matched_words']}")
    
    if result['hate_speech']['detected']:
        print(f"  🚫 Hate speech detected!")
        print(f"  Target groups: {result['hate_speech']['target_groups']}")
        
        signals = result['hate_speech']['signals']
        if signals['slurs']['detected']:
            print(f"  Slurs: {signals['slurs']['matches']}")
        if signals['group_dehumanization']['detected']:
            print(f"  Dehumanization: {signals['group_dehumanization']['dehumanizing_terms']}")
