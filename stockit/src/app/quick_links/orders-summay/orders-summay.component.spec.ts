import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrdersSummayComponent } from './orders-summay.component';

describe('OrdersSummayComponent', () => {
  let component: OrdersSummayComponent;
  let fixture: ComponentFixture<OrdersSummayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OrdersSummayComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OrdersSummayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
