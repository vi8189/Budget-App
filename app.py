from flask import Flask, request, jsonify, render_template
from db import db, Category, Entry, Expenditure
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables within app context during initialization
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/budget')
def budget():
    return render_template('budget.html')

@app.route('/expenditure')
def expenditure():
    return render_template('expenditure.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        year = request.args.get('year', type=int)
        cost_center = request.args.get('cost_center')
        if not year or year < 2000 or year > 2100:
            return jsonify({'error': 'Invalid year'}), 400

        categories = Category.query.filter_by(cost_center=cost_center).all()
        result = []

        for category in categories:
            entries = Entry.query.filter_by(category_id=category.id, year=year).all()
            entry_list = [{
                'id': entry.id,
                'description': entry.description,
                'jan': entry.jan,
                'feb': entry.feb,
                'mar': entry.mar,
                'apr': entry.apr,
                'may': entry.may,
                'jun': entry.jun,
                'jul': entry.jul,
                'aug': entry.aug,
                'sep': entry.sep,
                'oct': entry.oct,
                'nov': entry.nov,
                'dec': entry.dec
            } for entry in entries]

            result.append({
                'id': category.id,
                'name': category.name,
                'entries': entry_list
            })

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['POST'])
def create_category():
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'year' not in data or 'cost_center' not in data:
            return jsonify({'error': 'Name, year and cost_center are required'}), 400

        # Create new category with all required fields
        category = Category(
            name=data['name'],
            cost_center=data['cost_center'],
            year=data['year']  # Add the year field
        )
        
        db.session.add(category)
        db.session.commit()

        return jsonify({
            'id': category.id, 
            'name': category.name,
            'cost_center': category.cost_center,
            'year': category.year
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500

@app.route('/api/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    try:
        category = Category.query.get_or_404(category_id)
        data = request.get_json()

        if not data or 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400

        category.name = data['name']
        db.session.commit()
        return jsonify({'id': category.id, 'name': category.name})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500


@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        category = Category.query.get_or_404(category_id)
        
        # Delete all expenditures in this category
        Expenditure.query.filter_by(category_id=category_id).delete()
        
        # Delete all entries in this category
        Entry.query.filter_by(category_id=category_id).delete()
        
        # Delete the category
        db.session.delete(category)
        db.session.commit()
        return '', 204
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500

@app.route('/api/entries', methods=['POST'])
def create_entry():
    try:
        data = request.get_json()
        required_fields = ['description', 'category_id', 'year', 'cost_center']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Create budget entry
        entry = Entry(
            description=data['description'],
            category_id=data['category_id'],
            year=data['year'],
            cost_center=data['cost_center'],
            jan=data.get('jan', 0),
            feb=data.get('feb', 0),
            mar=data.get('mar', 0),
            apr=data.get('apr', 0),
            may=data.get('may', 0),
            jun=data.get('jun', 0),
            jul=data.get('jul', 0),
            aug=data.get('aug', 0),
            sep=data.get('sep', 0),
            oct=data.get('oct', 0),
            nov=data.get('nov', 0),
            dec=data.get('dec', 0)
        )
        db.session.add(entry)

        # Create corresponding expenditure entry
        expenditure = Expenditure(
            description=data['description'],
            category_id=data['category_id'],
            year=data['year'],
            cost_center=data['cost_center'],
            jan=0, feb=0, mar=0, apr=0, may=0, jun=0,
            jul=0, aug=0, sep=0, oct=0, nov=0, dec=0,
            jan_note='', feb_note='', mar_note='', apr_note='', may_note='', jun_note='',
            jul_note='', aug_note='', sep_note='', oct_note='', nov_note='', dec_note=''
        )
        db.session.add(expenditure)

        db.session.commit()

        return jsonify({
            'id': entry.id,
            'description': entry.description,
            'category_id': entry.category_id,
            'year': entry.year,
            'cost_center': entry.cost_center,
            'jan': entry.jan,
            'feb': entry.feb,
            'mar': entry.mar,
            'apr': entry.apr,
            'may': entry.may,
            'jun': entry.jun,
            'jul': entry.jul,
            'aug': entry.aug,
            'sep': entry.sep,
            'oct': entry.oct,
            'nov': entry.nov,
            'dec': entry.dec
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500

@app.route('/api/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    try:
        entry = Entry.query.get_or_404(entry_id)
        data = request.get_json()

        # Update entry description
        if 'description' in data:
            old_description = entry.description
            new_description = data['description']
            entry.description = new_description
            
            # Update corresponding expenditure description
            expenditure = Expenditure.query.filter_by(
                category_id=entry.category_id,
                year=entry.year,
                description=old_description,
                cost_center=entry.cost_center
            ).first()
            
            if expenditure:
                expenditure.description = new_description

        # Update monthly values
        for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                      'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
            if month in data:
                setattr(entry, month, data.get(month, 0))

        db.session.commit()
        return jsonify({
            'id': entry.id,
            'description': entry.description,
            'category_id': entry.category_id,
            'year': entry.year,
            'cost_center': entry.cost_center,
            'jan': entry.jan,
            'feb': entry.feb,
            'mar': entry.mar,
            'apr': entry.apr,
            'may': entry.may,
            'jun': entry.jun,
            'jul': entry.jul,
            'aug': entry.aug,
            'sep': entry.sep,
            'oct': entry.oct,
            'nov': entry.nov,
            'dec': entry.dec
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500

@app.route('/api/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    try:
        entry = Entry.query.get_or_404(entry_id)
        
        # Find and delete corresponding expenditure
        expenditure = Expenditure.query.filter_by(
            category_id=entry.category_id,
            year=entry.year,
            description=entry.description
        ).first()
        
        if expenditure:
            db.session.delete(expenditure)
        
        # Delete the entry
        db.session.delete(entry)
        db.session.commit()
        return '', 204
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500

@app.route('/api/expenditures/categories', methods=['GET'])
def get_expenditure_categories():
    try:
        year = request.args.get('year', type=int)
        cost_center = request.args.get('cost_center')
        
        print(f"Fetching expenditures for year: {year}, cost_center: {cost_center}")  # Debug log
        
        if not year or year < 2000 or year > 2100:
            return jsonify({'error': 'Invalid year'}), 400

        categories = Category.query.filter_by(cost_center=cost_center).all()
        result = []

        for category in categories:
            expenditures = Expenditure.query.filter_by(
                category_id=category.id,
                year=year,
                cost_center=cost_center
            ).all()
            
            print(f"Found {len(expenditures)} expenditures for category {category.name}")  # Debug log
            
            result.append({
                'id': category.id,
                'name': category.name,
                'entries': [{
                    'id': e.id,
                    'description': e.description,
                    # 'cost_center': e.cost_center,
                    'jan': e.jan,
                    'feb': e.feb,
                    'mar': e.mar,
                    'apr': e.apr,
                    'may': e.may,
                    'jun': e.jun,
                    'jul': e.jul,
                    'aug': e.aug,
                    'sep': e.sep,
                    'oct': e.oct,
                    'nov': e.nov,
                    'dec': e.dec,
                    'jan_note': e.jan_note,
                    'feb_note': e.feb_note,
                    'mar_note': e.mar_note,
                    'apr_note': e.apr_note,
                    'may_note': e.may_note,
                    'jun_note': e.jun_note,
                    'jul_note': e.jul_note,
                    'aug_note': e.aug_note,
                    'sep_note': e.sep_note,
                    'oct_note': e.oct_note,
                    'nov_note': e.nov_note,
                    'dec_note': e.dec_note
                } for e in expenditures]
            })

        return jsonify(result)
    except Exception as e:
        print(f"Error in get_expenditure_categories: {str(e)}")  # Debug log
        return jsonify({'error': str(e)}), 500
        return jsonify(result)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenditures/update', methods=['POST'])
def update_expenditure_data():
    try:
        data_array = request.get_json()
        if not isinstance(data_array, list):
            return jsonify({'error': 'Expected an array of expenditure data'}), 400

        for data in data_array:
            # Validate required fields
            required_fields = ['categoryId', 'description', 'month', 'value', 'note', 'year', 'cost_center']
            if not all(field in data for field in required_fields):
                return jsonify({'error': f'Missing required fields in entry: {data}'}), 400

            # Find expenditure record
            expenditure = Expenditure.query.filter_by(
                category_id=data['categoryId'],
                description=data['description'],
                year=data['year'],
                cost_center=data['cost_center']
            ).first()

            if not expenditure:
                # Create new expenditure record if it doesn't exist
                expenditure = Expenditure(
                    category_id=data['categoryId'],
                    description=data['description'],
                    year=data['year'],
                    cost_center=data['cost_center']
                )
                db.session.add(expenditure)

            # Update the value and note for the specific month
            month = data['month']
            setattr(expenditure, month, float(data['value']))
            setattr(expenditure, f"{month}_note", data['note'])

        db.session.commit()
        return jsonify({'success': True})

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/data')
def get_data():
    cost_center = request.args.get('cost_center')
    categories = Category.query.filter_by(cost_center=cost_center).all()
    category_ids = [category.id for category in categories]
    entries = Entry.query.filter(Entry.category_id.in_(category_ids)).all()
    expenditures = Expenditure.query.filter(Expenditure.category_id.in_(category_ids)).all()
    
    categories_data = [{'id': c.id, 'name': c.name} for c in categories]
    entries_data = [{'description': e.description, 'year': e.year, 'jan': e.jan, 'feb': e.feb, 'mar': e.mar, 'apr': e.apr, 'may': e.may, 'jun': e.jun, 'jul': e.jul, 'aug': e.aug, 'sep': e.sep, 'oct': e.oct, 'nov': e.nov, 'dec': e.dec} for e in entries]
    expenditures_data = [{'description': e.description, 'year': e.year, 'jan': e.jan, 'jan_note': e.jan_note, 'feb': e.feb, 'feb_note': e.feb_note, 'mar': e.mar, 'mar_note': e.mar_note, 'apr': e.apr, 'apr_note': e.apr_note, 'may': e.may, 'may_note': e.may_note, 'jun': e.jun, 'jun_note': e.jun_note, 'jul': e.jul, 'jul_note': e.jul_note, 'aug': e.aug, 'aug_note': e.aug_note, 'sep': e.sep, 'sep_note': e.sep_note, 'oct': e.oct, 'oct_note': e.oct_note, 'nov': e.nov, 'nov_note': e.nov_note, 'dec': e.dec, 'dec_note': e.dec_note} for e in expenditures]
    
    return jsonify({'categories': categories_data, 'entries': entries_data, 'expenditures': expenditures_data})

@app.route('/api/analysis')
def get_analysis():
    try:
        year = request.args.get('year', type=int)
        cost_center = request.args.get('cost_center')
        if not year or year < 2000 or year > 2100:
            return jsonify({'error': 'Invalid year'}), 400

        # Get all categories for the year and cost center
        categories = Category.query.filter_by(cost_center=cost_center).all()
        monthly_budget = {i: 0 for i in range(1, 13)}  # Initialize monthly totals
        monthly_expenditure = {i: 0 for i in range(1, 13)}
        
        # Calculate monthly totals across all categories
        for category in categories:
            # Sum up budget entries
            entries = Entry.query.filter_by(category_id=category.id, year=year).all()
            for entry in entries:
                monthly_budget[1] += entry.jan or 0
                monthly_budget[2] += entry.feb or 0
                monthly_budget[3] += entry.mar or 0
                monthly_budget[4] += entry.apr or 0
                monthly_budget[5] += entry.may or 0
                monthly_budget[6] += entry.jun or 0
                monthly_budget[7] += entry.jul or 0
                monthly_budget[8] += entry.aug or 0
                monthly_budget[9] += entry.sep or 0
                monthly_budget[10] += entry.oct or 0
                monthly_budget[11] += entry.nov or 0
                monthly_budget[12] += entry.dec or 0

            # Sum up expenditure entries
            expenditures = Expenditure.query.filter_by(category_id=category.id, year=year).all()
            for expenditure in expenditures:
                monthly_expenditure[1] += expenditure.jan or 0
                monthly_expenditure[2] += expenditure.feb or 0
                monthly_expenditure[3] += expenditure.mar or 0
                monthly_expenditure[4] += expenditure.apr or 0
                monthly_expenditure[5] += expenditure.may or 0
                monthly_expenditure[6] += expenditure.jun or 0
                monthly_expenditure[7] += expenditure.jul or 0
                monthly_expenditure[8] += expenditure.aug or 0
                monthly_expenditure[9] += expenditure.sep or 0
                monthly_expenditure[10] += expenditure.oct or 0
                monthly_expenditure[11] += expenditure.nov or 0
                monthly_expenditure[12] += expenditure.dec or 0

        # Calculate category totals
        budget_totals = list(monthly_budget.values())
        expenditure_totals = list(monthly_expenditure.values())

        return jsonify({
            'labels': ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December'],
            'budgetTotals': budget_totals,
            'expenditureTotals': expenditure_totals,
            'monthlyBudget': monthly_budget,
            'monthlyExpenditure': monthly_expenditure
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)