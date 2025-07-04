#!/usr/bin/env python3
"""
Setup script for Williamsburg News Application
Initializes database and loads demo data
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_application():
    """Initialize the application with demo data"""
    print("🏛️  Williamsburg Local News - Setup Script")
    print("=" * 50)
    
    try:
        # Import application components
        from app import create_app
        from models import db, MeetingAgenda
        from demo_data import get_demo_meetings
        from ai_service import AIService
        from datetime import datetime
        
        # Create Flask app
        print("📱 Creating Flask application...")
        app = create_app()
        
        with app.app_context():
            # Initialize database
            print("🗄️  Initializing database...")
            db.create_all()
            print("   ✅ Database tables created")
            
            # Check if we already have data
            existing_count = MeetingAgenda.query.count()
            if existing_count > 0:
                print(f"   ℹ️  Found {existing_count} existing meetings")
            else:
                # Load demo data
                print("📋 Loading demo meeting data...")
                demo_meetings = get_demo_meetings()
                added_count = 0
                
                for meeting_data in demo_meetings:
                    agenda = MeetingAgenda(
                        meeting_date=meeting_data['meeting_date'],
                        meeting_title=meeting_data['meeting_title'],
                        original_url=meeting_data['original_url'],
                        agenda_content=meeting_data['agenda_content'],
                        source=meeting_data['source']
                    )
                    
                    db.session.add(agenda)
                    added_count += 1
                    print(f"   📄 Added: {meeting_data['meeting_title'][:60]}...")
                
                db.session.commit()
                print(f"   ✅ Loaded {added_count} demo meetings")
            
            # Generate AI summaries
            print("🤖 Generating AI summaries...")
            unprocessed = MeetingAgenda.query.filter(
                MeetingAgenda.is_processed == False
            ).all()
            
            if unprocessed:
                ai_service = AIService()
                processed_count = 0
                
                for agenda in unprocessed:
                    if not agenda.agenda_content or len(agenda.agenda_content.strip()) < 50:
                        continue
                    
                    print(f"   🔄 Processing: {agenda.meeting_title[:50]}...")
                    
                    try:
                        ai_result = ai_service.generate_summary(
                            agenda.agenda_content,
                            agenda.meeting_title,
                            str(agenda.meeting_date)
                        )
                        
                        agenda.ai_summary = ai_result['summary']
                        agenda.ai_highlights = ai_result['highlights']
                        agenda.summary_generated_at = datetime.utcnow()
                        agenda.is_processed = True
                        
                        processed_count += 1
                        print(f"      ✅ Summary generated")
                        
                    except Exception as e:
                        print(f"      ⚠️  Error: {e}")
                        continue
                
                db.session.commit()
                print(f"   ✅ Generated summaries for {processed_count} meetings")
            else:
                print("   ℹ️  All meetings already processed")
            
            # Final statistics
            total_meetings = MeetingAgenda.query.count()
            processed_meetings = MeetingAgenda.query.filter(MeetingAgenda.is_processed == True).count()
            williamsburg_count = MeetingAgenda.query.filter(MeetingAgenda.source == 'williamsburg').count()
            jamescity_count = MeetingAgenda.query.filter(MeetingAgenda.source == 'jamescity').count()
            
            print("\n📊 Application Statistics:")
            print(f"   📋 Total meetings: {total_meetings}")
            print(f"   ✅ Processed: {processed_meetings}")
            print(f"   🏛️  Williamsburg: {williamsburg_count}")
            print(f"   🏞️  James City: {jamescity_count}")
            
        print("\n🎉 Setup completed successfully!")
        print("\n🚀 To start the application:")
        print("   python app.py")
        print("\n🌐 Then visit: http://localhost:5000")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    """Test basic imports"""
    try:
        from flask import Flask
        print("✓ Flask imported")
        
        import sqlite3
        print("✓ SQLite available")
        
        from datetime import datetime
        print("✓ Datetime imported")
        
        return True
    except Exception as e:
        print(f"✗ Basic import error: {e}")
        return False

def create_simple_app():
    """Create a minimal Flask app for testing"""
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///williamsburg_news.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-key-for-testing'
    
    @app.route('/')
    def home():
        return jsonify({
            'message': 'Williamsburg News App is running!',
            'status': 'healthy'
        })
        
    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'})
    
    return app

def setup_database():
    """Set up database with demo data"""
    try:
        # Import after we know basic imports work
        from models import db, MeetingAgenda
        from demo_data import get_demo_meetings
        from ai_service import AIService
        from datetime import datetime
        
        app = create_simple_app()
        
        # Initialize database
        db.init_app(app)
        
        with app.app_context():
            # Create tables
            db.create_all()
            print("✓ Database tables created")
            
            # Check if demo data already exists
            existing_count = MeetingAgenda.query.count()
            if existing_count > 0:
                print(f"✓ Found {existing_count} existing meetings")
                return app
            
            # Load demo data
            demo_meetings = get_demo_meetings()
            print(f"✓ Generated {len(demo_meetings)} demo meetings")
            
            ai_service = AIService()
            added_count = 0
            
            for meeting_data in demo_meetings:
                # Create meeting record
                agenda = MeetingAgenda(
                    meeting_date=meeting_data['meeting_date'],
                    meeting_title=meeting_data['meeting_title'],
                    original_url=meeting_data['original_url'],
                    agenda_content=meeting_data['agenda_content'],
                    source=meeting_data['source']
                )
                
                # Generate summary
                try:
                    ai_result = ai_service.generate_summary(
                        agenda.agenda_content,
                        agenda.meeting_title,
                        str(agenda.meeting_date)
                    )
                    
                    agenda.ai_summary = ai_result['summary']
                    agenda.ai_highlights = ai_result['highlights']
                    agenda.summary_generated_at = datetime.utcnow()
                    agenda.is_processed = True
                    
                except Exception as e:
                    print(f"  Warning: Could not generate AI summary for {meeting_data['meeting_title']}: {e}")
                    agenda.is_processed = False
                
                db.session.add(agenda)
                added_count += 1
            
            db.session.commit()
            print(f"✓ Added {added_count} meetings to database")
            
            return app
            
    except Exception as e:
        print(f"✗ Database setup error: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main setup function"""
    print("Williamsburg News App Setup")
    print("=" * 30)
    
    # Test basic functionality
    if not test_basic_imports():
        return False
    
    # Set up database and demo data
    app = setup_database()
    if not app:
        return False
    
    print("\n✓ Setup completed successfully!")
    print("\nYou can now run:")
    print("  python app.py")
    print("\nOr test the API:")
    print("  curl http://localhost:5000/health")
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)
