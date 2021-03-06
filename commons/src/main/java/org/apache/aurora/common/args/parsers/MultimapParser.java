/**
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.aurora.common.args.parsers;

import java.lang.reflect.Type;
import java.util.List;

import com.google.common.base.Splitter;
import com.google.common.collect.ImmutableList;
import com.google.common.collect.ImmutableMultimap;
import com.google.common.collect.Multimap;
import com.google.common.reflect.TypeToken;

import org.apache.aurora.common.args.ArgParser;
import org.apache.aurora.common.args.Parser;
import org.apache.aurora.common.args.ParserOracle;
import org.apache.aurora.common.args.Parsers;

import static com.google.common.base.Preconditions.checkArgument;

/**
 * Multimap parser.
 */
@ArgParser
public class MultimapParser extends TypeParameterizedParser<Multimap<?, ?>> {

  private static final Splitter KEY_VALUE_SPLITTER =
      Splitter.on("=").trimResults().omitEmptyStrings();

  public MultimapParser() {
    super(2);
  }

  @SuppressWarnings("unchecked")
  @Override
  Multimap<?, ?> doParse(ParserOracle parserOracle, String raw, List<Type> typeParams) {
    Type keyType = typeParams.get(0);
    Parser<?> keyParser = parserOracle.get(TypeToken.of(keyType));

    Type valueType = typeParams.get(1);
    Parser<?> valueParser = parserOracle.get(TypeToken.of(valueType));

    ImmutableMultimap.Builder<Object, Object> multimapBuilder = ImmutableMultimap.builder();
    for (String keyAndValue : Parsers.MULTI_VALUE_SPLITTER.split(raw)) {
      List<String> fields = ImmutableList.copyOf(KEY_VALUE_SPLITTER.split(keyAndValue));
      checkArgument(fields.size() == 2, "Failed to parse key/value pair: " + keyAndValue);
      multimapBuilder.put(
          keyParser.parse(parserOracle, keyType, fields.get(0)),
          valueParser.parse(parserOracle, valueType, fields.get(1)));
    }

    return multimapBuilder.build();
  }
}
