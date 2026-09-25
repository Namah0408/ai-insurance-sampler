import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerResponse


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
):
    existing_customer = (
        db.query(Customer)
        .filter(
            Customer.customer_reference
            == customer_data.customer_reference
        )
        .first()
    )

    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer reference already exists",
        )

    customer = Customer(
        customer_reference=customer_data.customer_reference,
        full_name=customer_data.full_name,
        date_of_birth=customer_data.date_of_birth,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


@router.get(
    "/",
    response_model=list[CustomerResponse],
)
def get_customers(
    db: Session = Depends(get_db),
):
    return db.query(Customer).order_by(Customer.created_at.desc()).all()


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer