import os
from PIL import Image as PILImage
from flask import Flask, render_template, redirect, url_for, flash, logging, request
from werkzeug.utils import secure_filename

from . import real_estate_bp
from .forms import HousingForm, SearchHousingForm
from .models import Housing, Image, Communication, Comfort, HousingType, RepairType
from app import db, login_manager
from app.users.models import User
from flask_login import login_required, current_user

@real_estate_bp.route('/', methods=['GET', 'POST'])
def get_housings():
    form = SearchHousingForm()

    # Заповнення опцій для SelectField та MultiCheckboxField
    form.type.choices = [(t.id, t.name) for t in HousingType.query.all()]
    form.repair.choices = [(r.id, r.name) for r in RepairType.query.all()]
    form.communications.choices = [(c.id, c.name) for c in Communication.query.all()]
    form.comforts.choices = [(c.id, c.name) for c in Comfort.query.all()]

    housings = Housing.query

    if form.is_submitted():
        # Фільтрація за ціною
        if form.min_price.data:
            housings = housings.filter(Housing.price >= form.min_price.data)
        if form.max_price.data:
            housings = housings.filter(Housing.price <= form.max_price.data)

        # Фільтрація за площею
        if form.min_area.data:
            housings = housings.filter(Housing.area >= form.min_area.data)
        if form.max_area.data:
            housings = housings.filter(Housing.area <= form.max_area.data)

        # Фільтрація за кількістю кімнат
        if form.rooms.data:
            housings = housings.filter(Housing.rooms == form.rooms.data)

        # Фільтрація за типом житла
        if form.type.data:
            housings = housings.filter(Housing.housing_type_id == form.type.data)

        # Фільтрація за типом ремонту
        if form.repair.data:
            housings = housings.filter(Housing.repair_type_id == form.repair.data)

        # Фільтрація за комунікаціями (всі вибрані)
        if form.communications.data:
            for communication_id in form.communications.data:
                housings = housings.filter(Housing.communications.any(id=communication_id))

        # Фільтрація за зручностями (всі вибрані)
        if form.comforts.data:
            for comfort_id in form.comforts.data:
                housings = housings.filter(Housing.comforts.any(id=comfort_id))

        # Сортування
        sort_by = form.sort_by.data
        if sort_by == 'price':
            housings = housings.order_by(Housing.price.asc())
        elif sort_by == 'rooms':
            housings = housings.order_by(Housing.rooms.asc())
        elif sort_by == 'area':
            housings = housings.order_by(Housing.area.asc())
        else:
            housings = housings.order_by(Housing.created.desc())

        flash('Filter successfully applied', 'success')

    housings = housings.all()
    return render_template('housings.html', housings=housings, form=form)

@real_estate_bp.route('/housing/<int:housing_id>')
def get_housing(housing_id):
    housing = Housing.query.get(housing_id)
    return render_template('housing.html', housing=housing)

def save_image(image, output_size=(300, 200)):
    filename = secure_filename(image.filename)
    image_path = os.path.join(real_estate_bp.root_path, 'static/img', filename)
    img = PILImage.open(image)
    img = img.resize(output_size)
    img.save(image_path)
    return filename


@real_estate_bp.route('/add_housing', methods=['GET', 'POST'])
@login_required
def add_housing():
    form = HousingForm()

    # Динамічне наповнення списків для SelectField та MultiCheckboxField
    form.type.choices = [(t.id, t.name) for t in HousingType.query.all()]
    form.repair.choices = [(r.id, r.name) for r in RepairType.query.all()]
    form.communications.choices = [(c.id, c.name) for c in Communication.query.all()]
    form.comforts.choices = [(c.id, c.name) for c in Comfort.query.all()]

    if form.validate_on_submit():
        images = []
        for image in form.images.data:
            if image:
                filename = save_image(image)
                image_record = Image(filename=filename)
                db.session.add(image_record)
                db.session.commit()
                images.append(image_record)
        housing = Housing(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            address=form.address.data,
            area=form.area.data,
            rooms=form.rooms.data,
            housing_type_id=form.type.data,
            repair_type_id=form.repair.data,
            communications=[Communication.query.get(comm_id) for comm_id in form.communications.data],
            comforts=[Comfort.query.get(comf_id) for comf_id in form.comforts.data],
            images=images,
            user_id = current_user.id
        )
        db.session.add(housing)
        db.session.commit()
        flash('Housing has been added successfully', 'success')
        return redirect(url_for('real_estate.get_housings'))

    return render_template('add_housing.html', form=form)

@real_estate_bp.route('/edit_housing/<int:housing_id>', methods=['GET', 'POST'])
@login_required
def edit_housing(housing_id):
    housing = Housing.query.get_or_404(housing_id)
    if housing.user_id != current_user.id:
        flash('You are not authorized to edit this housing.', 'danger')
        return redirect(url_for('real_estate.get_housings'))
    form = HousingForm(obj=housing)
    # Динамічне наповнення списків для SelectField та MultiCheckboxField
    form.type.choices = [(t.id, t.name) for t in HousingType.query.all()]
    form.repair.choices = [(r.id, r.name) for r in RepairType.query.all()]
    form.communications.choices = [(c.id, c.name) for c in Communication.query.all()]
    form.comforts.choices = [(c.id, c.name) for c in Comfort.query.all()]

    # Встановлення значень для полів форми з об'єкта Housing
    form.type.data = housing.housing_type_id
    form.repair.data = housing.repair_type_id
    form.communications.data = [comm.id for comm in housing.communications]
    form.comforts.data = [comf.id for comf in housing.comforts]

    if form.validate_on_submit():
        housing.title = form.title.data
        housing.description = form.description.data
        housing.price = form.price.data
        housing.address = form.address.data
        housing.area = form.area.data
        housing.rooms = form.rooms.data
        housing.housing_type_id = form.type.data
        housing.repair_type_id = form.repair.data
        housing.communications = [Communication.query.get(comm_id) for comm_id in form.communications.data]
        housing.comforts = [Comfort.query.get(comf_id) for comf_id in form.comforts.data]

        db.session.commit()
        flash('Housing has been updated successfully', 'success')
        return redirect(url_for('real_estate.get_housing', housing_id=housing.id))
    return render_template('edit_housing.html', form=form, housing=housing)


@real_estate_bp.route('/delete_housing/<int:housing_id>', methods=['POST'])
@login_required
def delete_housing(housing_id):
    housing = Housing.query.get_or_404(housing_id)
    if housing.user_id != current_user.id:
        flash('You are not authorized to delete this housing.', 'danger')
        return redirect(url_for('real_estate.get_housings'))
    db.session.delete(housing)
    db.session.commit()
    flash('Housing has been deleted successfully', 'success')
    return redirect(url_for('real_estate.get_housings'))

@real_estate_bp.route('/delete_photo/<int:photo_id>', methods=['POST'])
def delete_photo(photo_id):
    image = Image.query.get(photo_id)
    if image:
        db.session.delete(image)
        db.session.commit()
        flash('Photo has been deleted successfully', 'success')
    else:
        flash('Photo not found', 'danger')
    return redirect(request.referrer)