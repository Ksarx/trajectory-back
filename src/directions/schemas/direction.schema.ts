import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';

@Schema()
export class Direction {
  @Prop()
  id: number;

  @Prop()
  code: string;

  @Prop()
  name: string;

  @Prop()
  level: string;

  @Prop()
  faculty: string;

  @Prop()
  description: string;

  @Prop([Number])
  idJobs: number[];

  @Prop([
    {
      semNumber: { type: Number },
      disciplines: { type: [String] },
    },
  ])
  semesters: {
    semNumber: number;
    disciplines: string[];
  }[];
}

export const DirectionSchema = SchemaFactory.createForClass(Direction);
